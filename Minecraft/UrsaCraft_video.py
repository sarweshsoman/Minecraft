from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from enum import Enum

class BlockType(Enum):
    GRASS = 1
    STONE = 2
    BRICK = 3
    DIRT = 4

app = Ursina()
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture = load_texture('assets/dirt_block.png')
sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture.png')
punch_sound = Audio('assets/punch_sound.wav', loop=False, autoplay=False)
block_pick = BlockType.GRASS  # Default block type

window.fps_counter.enabled = False
window.exit_button.visible = False

def update():
    global block_pick

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

    block_mapping = {'1': BlockType.GRASS, '2': BlockType.STONE, '3': BlockType.BRICK, '4': BlockType.DIRT}
    for key, block_type in block_mapping.items():
        if held_keys[key]:
            block_pick = block_type

class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=0.5)

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                punch_sound.play()
                texture_mapping = {
                    BlockType.GRASS: grass_texture,
                    BlockType.STONE: stone_texture,
                    BlockType.BRICK: brick_texture,
                    BlockType.DIRT: dirt_texture
                }
                voxel = Voxel(position=self.position + mouse.normal, texture=texture_mapping[block_pick])

            if key == 'right mouse down':
                punch_sound.play()
                destroy(self)

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=300,  # Adjusted scale to increase the sky size
            double_sided=True)

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/arm',
            texture=arm_texture,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6))

    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)

# Increased world size
WORLD_SIZE = 30

for z in range(WORLD_SIZE):
    for x in range(WORLD_SIZE):
        voxel = Voxel(position=(x, 0, z))

player = FirstPersonController()
sky = Sky()
hand = Hand()

app.run()
