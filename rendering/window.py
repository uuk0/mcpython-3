import pyglet
import globals as G
import math
import world.WorldAccess
import util.vector, util.vertices
import texture.BlockItemFactory

from pyglet.window import key, mouse

import gui.ItemStack

import gui.TextDraw


class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        G.window = self

        super(Window, self).__init__(*args, **kwargs)

        # useful values

        self.on_ground = False

        # timouts

        self.time_since_on_ground = 0

        # Whether or not the window exclusively captures the mouse.
        self.exclusive = False

        # When flying gravity has no effect and speed is increased.
        self.flying = False

        # Strafing is moving lateral to the direction you are facing,
        # e.g. moving to the left or right while continuing to face forward.
        #
        # First element is -1 when moving forward, 1 when moving back, and 0
        # otherwise. The second element is -1 when moving left, 1 when moving
        # right, and 0 otherwise.
        self.strafe = [0, 0]

        self.is_pressing_space = False

        # Current (x, y, z) position in the world, specified with floats. Note
        # that, perhaps unlike in math class, the y-axis is the vertical axis.
        self.position = (0, 50, 0)

        # First element is rotation of the player in the x-z plane (ground
        # plane) measured from the z-axis down. The second is the rotation
        # angle from the ground plane up. Rotation is in degrees.
        #
        # The vertical plane rotation ranges from -90 (looking straight down) to
        # 90 (looking straight up). The horizontal rotation range is unbounded.
        self.rotation = (0, 0)

        # Which sector the player is currently in.
        self.sector = None

        # The crosshairs at the center of the screen.
        self.reticle = None

        # Velocity in the y (upward) direction.
        self.dy = 0

        # Convenience list of num keys.
        self.num_keys = [
            key._1, key._2, key._3, key._4, key._5,
            key._6, key._7, key._8, key._9]

        # Instance of the model that handles the world.
        self.worldaccess = world.WorldAccess.WorldAccess(seed=G.CONFIG["seed"])

        self.counter = 0

        # The label that is displayed in the top left of the canvas.
        self.label = pyglet.text.Label('', font_name='Arial', font_size=9,
            x=10, y=self.height - 10, anchor_x='left', anchor_y='top',
            color=(0, 0, 0, 255))

        # This call schedules the `update()` method to be called
        # TICKS_PER_SEC. This is the main game event loop.
        pyglet.clock.schedule_interval(self.update, 1.0 / G.CONFIG["TICKS_PER_SEC"])

    def set_exclusive_mouse(self, exclusive):
        """ If `exclusive` is True, the game will capture the mouse, if False
        the game will ignore the mouse.

        """
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def get_sight_vector(self):
        """ Returns the current line of sight vector indicating the direction
        the player is looking.

        """
        x, y = self.rotation
        # y ranges from -90 to 90, or -pi/2 to pi/2, so m ranges from 0 to 1 and
        # is 1 when looking ahead parallel to the ground and 0 when looking
        # straight up or down.
        m = math.cos(math.radians(y))
        # dy ranges from -1 to 1 and is -1 when looking straight down and 1 when
        # looking straight up.
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return dx, dy, dz

    def get_motion_vector(self):
        """ Returns the current motion vector indicating the velocity of the
        player.

        Returns
        -------
        vector : tuple of len 3
            Tuple containing the velocity in x, y, and z respectively.

        """
        if any(self.strafe):
            x, y = self.rotation
            strafe = math.degrees(math.atan2(*self.strafe))
            y_angle = math.radians(y)
            x_angle = math.radians(x + strafe)
            if self.flying:
                m = math.cos(y_angle)
                dy = math.sin(y_angle)
                if self.strafe[1]:
                    # Moving left or right.
                    dy = 0.0
                    m = 1
                if self.strafe[0] > 0:
                    # Moving backwards.
                    dy *= -1
                # When you are flying up or down, you have less left and right
                # motion.
                dx = math.cos(x_angle) * m
                dz = math.sin(x_angle) * m
            else:
                dy = 0.0
                dx = math.cos(x_angle)
                dz = math.sin(x_angle)
        else:
            dy = 0.0
            dx = 0.0
            dz = 0.0
        return dx, dy, dz

    def update(self, dt):
        """ This method is scheduled to be called repeatedly by the pyglet
        clock.

        Parameters
        ----------
        dt : float
            The change in time since the last call.

        """
        # todo: need we these line?
        # self.model.process_queue()
        if self.on_ground:
            self.time_since_on_ground += 1
        sector = util.vector.sectorize(self.position)
        if sector != self.sector:
            self.worldaccess.change_sectors(self.sector, sector)
            # if self.sector is None:
            #     self.model.process_entire_queue()
            self.sector = sector
        m = 8
        dt = min(dt, 0.2)
        if texture.BlockItemFactory.dummyinventoryblockitemfactory not in G.inventoryhandler.visable_inventorys:
            for _ in range(m):
                self._update(dt / m)
        if self.dy < 0.1 and self.is_pressing_space and self.on_ground: # and self.time_since_on_ground > 0.5:
            self.dy = G.CONFIG["JUMP_SPEED"]
        # print(self.time_since_on_ground)
        if G.inventoryhandler.should_game_freeze():
            G.inventoryhandler.send_event("update", dt)
        if self.position[1] < -100:
            G.player.kill()

    def _update(self, dt):
        """ Private implementation of the `update()` method. This is where most
        of the motion logic lives, along with gravity and collision detection.

        Parameters
        ----------
        dt : float
            The change in time since the last call.

        """
        # walking
        speed = G.CONFIG["FLYING_SPEED"] if self.flying else G.CONFIG["WALKING_SPEED"]
        d = dt * speed  # distance covered this tick.
        dx, dy, dz = self.get_motion_vector()
        # New position in space, before accounting for gravity.
        dx, dy, dz = dx * d, dy * d, dz * d
        # gravity
        if not self.flying:
            # Update your vertical speed: if you are falling, speed up until you
            # hit terminal velocity; if you are jumping, slow down until you
            # start falling.
            self.dy -= dt * G.CONFIG["GRAVITY"]
            self.dy = max(self.dy, -G.CONFIG["TERMINAL_VELOCITY"])
            dy += self.dy * dt
        # collisions
        x, y, z = self.position
        x, y, z = self.collide((x + dx, y + dy, z + dz), G.CONFIG["PLAYER_HEIGHT"])
        self.position = (x, y, z)

    def collide(self, position, height):
        """ Checks to see if the player at the given `position` and `height`
        is colliding with any blocks in the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position to check for collisions at.
        height : int or float
            The height of the player.

        Returns
        -------
        position : tuple of len 3
            The new position of the player taking into account collisions.

        """
        if G.player.gamemode == 3: return position
        # How much overlap with a dimension of a surrounding block you need to
        # have to count as a collision. If 0, touching terrain at all counts as
        # a collision. If .49, you sink into the ground, as if walking through
        # tall grass. If >= .5, you'll fall through the ground.
        pad = 0.25
        p = list(position)
        np = util.vector.normalize(position)
        for face in G.CONFIG["FACES"]:  # check all surrounding blocks
            face = tuple(face)
            for i in range(3):  # check each dimension independently
                if not face[i]:
                    continue
                # How much overlap you have with this dimension.
                d = (p[i] - np[i]) * face[i]
                if d < pad:
                    continue
                for dy in range(height):  # check each height
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    chunk = util.vector.sectorize(op)
                    chunkaccess = G.worldaccess.get_active_dimension_access().get_chunk_for(chunk, generate=False,
                                                                                            create=False)
                    if chunkaccess and (tuple(op) not in chunkaccess.world or
                                        chunkaccess.world[tuple(op)].can_player_walk_through()):
                        if face == (0, -1, 0):
                            self.on_ground = False
                            self.time_since_on_ground = 0
                        continue
                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        # You are colliding with the ground or ceiling, so stop
                        # falling / rising.
                        self.dy = 0
                    if face == (0, -1, 0):
                        self.on_ground = True
                        self.time_since_on_ground = 0
                    break
        return tuple(p)

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called when a mouse button is pressed. See pyglet docs for button
        amd modifier mappings.

        Parameters
        ----------
        x, y : int
            The coordinates of the mouse click. Always center of the screen if
            the mouse is captured.
        button : int
            Number representing mouse button that was clicked. 1 = left button,
            4 = right button.
        modifiers : int
            Number representing any modifying keys that were pressed when the
            mouse button was clicked.

        """
        if G.inventoryhandler.should_game_freeze():
            G.inventoryhandler.send_event("on_mouse_press", x, y, button, modifiers)
            return
        if self.exclusive:
            vector = self.get_sight_vector()
            block, previous, phit = G.worldaccess.hit_test(self.position, vector, exact_hit=True)
            iblock = G.worldaccess.get_block(block) if block else None
            if iblock and iblock.can_interact_with(
                    G.player.playerinventory.POSSIBLE_MODES["hotbar"].slots[G.player.selectedinventoryslot].get_stack(),
                    button, modifiers):
                v = iblock.on_interact_with(
                    G.player.playerinventory.POSSIBLE_MODES["hotbar"].slots[G.player.selectedinventoryslot].get_stack(),
                    button, modifiers
                )
                G.player.playerinventory.POSSIBLE_MODES["hotbar"].slots[G.player.selectedinventoryslot].set_stack(v[0])
                if not v[1]: return
            if (button == mouse.RIGHT) or \
                    ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)):
                # ON OSX, control + left click = right click.
                if previous and G.player.gamemode in [0, 1]:
                    slot = G.player.playerinventory.POSSIBLE_MODES["hotbar"].slots[G.player.selectedinventoryslot]
                    if slot.stack.item:
                        if slot.stack.item.has_block():
                            self.worldaccess.add_block(0, previous, slot.stack.item.getBlockName(),
                                                       arguments=[[], {"previous": block, "hitposition": phit}])
                            if G.player.gamemode == 0:
                                slot.stack.amount -= 1
                    elif slot.stack.itemname:
                        try:
                            self.worldaccess.add_block(0, previous, slot.stack.itemname,
                                                       arguments=[[], {"previous": block, "hitposition": phit}])
                            if G.player.gamemode == 0:
                                slot.stack.amount -= 1
                        except ValueError:
                            pass
            elif button == pyglet.window.mouse.LEFT and block:
                block = G.worldaccess.get_block(block)
                if G.player.gamemode != 3:
                    if G.player.gamemode != 1:
                        if block.isBrakeAble() and G.player.gamemode == 0:
                            G.worldaccess.remove_block(0, block.position)
                            drop = iblock.get_drop(
                                G.player.playerinventory.POSSIBLE_MODES["hotbar"].slots[
                                    G.player.selectedinventoryslot].get_stack())
                            for itemname in drop.keys():
                                G.player.add_to_free_place(itemname, drop[itemname])
                    else:
                        self.worldaccess.remove_block(0, block.position)
            elif button == pyglet.window.mouse.MIDDLE and block and G.player.gamemode == 1:
                block = G.worldaccess.get_block(block)
                slot = G.player.playerinventory.POSSIBLE_MODES["hotbar"].slots[G.player.selectedinventoryslot]
                slot.stack.set_item(block.getName())
        else:
            self.set_exclusive_mouse(True)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called when the player moves the mouse.

        Parameters
        ----------
        x, y : int
            The coordinates of the mouse click. Always center of the screen if
            the mouse is captured.
        dx, dy : float
            The movement of the mouse.

        """
        if G.inventoryhandler.should_game_freeze():
            G.inventoryhandler.send_event("on_mouse_motion", x, y, dx, dy)
            return
        if self.exclusive:
            m = 0.15
            x, y = self.rotation
            x, y = x + dx * m, y + dy * m
            y = max(-90, min(90, y))
            self.rotation = (x, y)

    def on_key_press(self, symbol, modifiers):
        """ Called when the player presses a key. See pyglet docs for key
        mappings.

        Parameters
        ----------
        symbol : int
            Number representing the key that was pressed.
        modifiers : int
            Number representing any modifying keys that were pressed.

        """
        if symbol == key.ESCAPE and G.inventoryhandler.should_game_freeze() and \
                texture.BlockItemFactory.dummyinventoryblockitemfactory not in G.inventoryhandler.visable_inventorys:
            G.inventoryhandler.remove_last_inventory_from_stack()
            return
        if G.inventoryhandler.should_game_freeze():
            G.inventoryhandler.send_event("on_key_press", symbol, modifiers)
            return
        if symbol == key.W:
            self.strafe[0] -= 1
        elif symbol == key.S:
            self.strafe[0] += 1
        elif symbol == key.A:
            self.strafe[1] -= 1
        elif symbol == key.D:
            self.strafe[1] += 1
        elif symbol == key.SPACE:
            if self.dy == 0:
                self.dy = G.CONFIG["JUMP_SPEED"]
                self.is_pressing_space = True
        elif symbol == key.ESCAPE:
            self.set_exclusive_mouse(False)
        elif symbol == key.TAB and G.player.gamemode == 1:
            self.flying = not self.flying
        elif symbol in self.num_keys:
            index = (symbol - self.num_keys[0])
            G.player.selectedinventoryslot = index
        elif symbol == key.E:
            if G.player.playerinventory.get_mode() == "hotbar":
                G.player.playerinventory.set_mode("inventory")
            else:
                G.player.playerinventory.set_mode("hotbar")
        elif symbol == key.R:
            self.strafe = [0, 0]
        elif symbol == key.T:
            G.inventoryhandler.show_inventory(G.player.chat)
        elif symbol == key.C and G.player.gamemode == 1:
            # for slot in G.player.playerinventory.POSSIBLE_MODES["inventory"].slots:
            #     slot.set_item("minecraft:stone")
            if modifiers & key.LSHIFT:
                self.counter += 1
                if self.counter > len(G.itemhandler.itemnames) // 9:
                    self.counter = 0
            elif modifiers & key.LALT:
                self.counter -= 1
                if self.counter < 0:
                    self.counter = len(G.itemhandler.itemnames) // 9
            else:
                items = []
                for i in range(self.counter*9, self.counter*9+9):
                    if len(G.itemhandler.itemnames) > i:
                        items.append(G.itemhandler.itemnames[i])
                for i, itemname in enumerate(items):
                    G.player.playerinventory.POSSIBLE_MODES["hotbar"].slots[i].\
                        set_stack(gui.ItemStack.ItemStack(itemname, 64))

    def on_key_release(self, symbol, modifiers):
        """ Called when the player releases a key. See pyglet docs for key
        mappings.

        Parameters
        ----------
        symbol : int
            Number representing the key that was pressed.
        modifiers : int
            Number representing any modifying keys that were pressed.

        """
        if G.inventoryhandler.should_game_freeze():
            G.inventoryhandler.send_event("on_key_release", symbol, modifiers)
            return
        if symbol == key.W:
            self.strafe[0] += 1
        elif symbol == key.S:
            self.strafe[0] -= 1
        elif symbol == key.A:
            self.strafe[1] += 1
        elif symbol == key.D:
            self.strafe[1] -= 1
        elif symbol == key.SPACE:
            self.is_pressing_space = False

    def on_resize(self, width, height):
        """ Called when the window is resized to a new `width` and `height`.

        """
        # label
        self.label.y = height - 10
        # reticle
        if self.reticle:
            self.reticle.delete()
        x, y = self.width // 2, self.height // 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(4, ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n)))

        if G.inventoryhandler.should_game_freeze():
            G.inventoryhandler.send_event("on_resize", width, height)

    def set_2d(self):
        """ Configure OpenGL to draw in 2d.

        """
        width, height = self.get_size()
        pyglet.gl.glDisable(pyglet.gl.GL_DEPTH_TEST)
        viewport = self.get_viewport_size()
        pyglet.gl.glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glOrtho(0, max(1, width), 0, max(1, height), -1, 1)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
        pyglet.gl.glLoadIdentity()

    def set_3d(self):
        """ Configure OpenGL to draw in 3d.

        """
        width, height = self.get_size()
        pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
        viewport = self.get_viewport_size()
        pyglet.gl.glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()
        pyglet.gl.gluPerspective(65.0, width / float(height), 0.1, 60.0)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
        pyglet.gl.glLoadIdentity()
        x, y = self.rotation
        pyglet.gl.glRotatef(x, 0, 1, 0)
        pyglet.gl.glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = self.position
        y += 0.5
        pyglet.gl.glTranslatef(-x, -y, -z)

    def on_draw(self):
        """ Called by pyglet to draw the canvas.

        """
        self.clear()
        self.set_3d()
        pyglet.gl.glColor3d(1, 1, 1)
        if G.inventoryhandler.should_game_freeze():
            G.inventoryhandler.send_event("draw_3d_start")
        self.worldaccess.draw_normal()
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        self.worldaccess.draw_alpha()
        if G.inventoryhandler.should_game_freeze():
            G.inventoryhandler.send_event("draw_3d_alpha")
        pyglet.gl.glDisable(pyglet.gl.GL_BLEND)
        if G.inventoryhandler.should_game_freeze():
            G.inventoryhandler.send_event("draw_3d_end")
        if G.player.gamemode != 3:
            self.draw_focused_block()
        self.set_2d()
        if G.inventoryhandler.should_game_freeze():
            G.inventoryhandler.send_event("draw_2d_start")
        self.worldaccess.draw_particle()
        if not G.inventoryhandler.should_game_freeze() and G.player.gamemode != 3:
            self.draw_reticle()
        self.draw_label()
        G.inventoryhandler.draw()
        if G.inventoryhandler.should_game_freeze():
            G.inventoryhandler.send_event("draw_2d_end")

    def draw_focused_block(self):
        """ Draw black edges around the block that is currently under the
        crosshairs.

        """
        if G.inventoryhandler.should_game_freeze(): return
        vector = self.get_sight_vector()
        block = G.worldaccess.hit_test(self.position, vector)[0]
        if block:
            x, y, z = block
            iblock = G.worldaccess.get_block(block)
            modelentry = G.modelhandler.modelindex[iblock.get_model_name()].entrys[iblock.get_active_model_index()]
            box = modelentry.data["box_size"] if "box_size" in modelentry.data else (0.5, 0.5, 0.5)
            rx, ry, rz = tuple(modelentry.data["relative_position"]) if "relative_position" in \
                                                                        modelentry.data else (0, 0, 0)
            vertex_data = util.vertices.cube_vertices(x+rx, y+ry, z+rz, *[x+0.01 for x in box])
            pyglet.gl.glColor3d(0, 0, 0)
            pyglet.gl.glPolygonMode(pyglet.gl.GL_FRONT_AND_BACK, pyglet.gl.GL_LINE)
            pyglet.graphics.draw(24, pyglet.gl.GL_QUADS, ('v3f/static', vertex_data))
            pyglet.gl.glPolygonMode(pyglet.gl.GL_FRONT_AND_BACK, pyglet.gl.GL_FILL)

    def draw_label(self):
        """ Draw the label in the top left of the screen.

        """
        x, y, z = self.position
        self.label.text = '%02d (%.2f, %.2f, %.2f)' % (
            pyglet.clock.get_fps(), x, y, z)
        sx, sy, sz = util.vector.normalize(self.position)
        # todo: reactivate binding
        if (sx, sz) in self.worldaccess.get_active_dimension_access().worldgenerationprovider.biomemap.map:
            self.label.text += ", biome: "+str(
                self.worldaccess.get_active_dimension_access().worldgenerationprovider.biomemap[(sx, sz)].getName())
        self.label.draw()

    def draw_reticle(self):
        """ Draw the crosshairs in the center of the screen.

        """
        if G.inventoryhandler.should_game_freeze(): return
        pyglet.gl.glColor3d(0, 0, 0)
        self.reticle.draw(pyglet.gl.GL_LINES)
        
    def on_hide(self):
        if not G.inventoryhandler.should_game_freeze():
            self.deactivate()

    def on_context_lost(self):
        if not G.inventoryhandler.should_game_freeze():
            self.deactivate()

    def on_context_state_lost(self):
        if not G.inventoryhandler.should_game_freeze():
            self.deactivate()

    def on_deactivate(self):
        if not G.inventoryhandler.should_game_freeze():
            self.deactivate()

    def deactivate(self):
        self.set_exclusive_mouse(False)
        self.strafe = [0, 0]
        self.is_pressing_space = False

