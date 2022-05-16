import io
import cv2
import gltflib
import numpy as np
from typing import Any, Dict, List, Tuple


class Service:

    def __init__(self, config: Dict[str, Any]):
        self._wc = config.get('wall_class', 9)
        self._wh = config.get('wall_height', 50)
        self._color = config.get('colorize', False)

    def _render_single_wall(self, x: int, y: int, z: int, t: int) \
            -> Tuple[List[Any], List[Any], List[Any]]:
        points = [ (0, 0, 0), (1, 0, 0), (0, 0, 1), (1, 0, 1),
                   (0, 1, 0), (1, 1, 0), (0, 1, 1), (1, 1, 1) ]

        triags = [ (0, 1, 2), (1, 2, 3), (4, 5, 6), (5, 6, 7),
                   (0, 2, 4), (2, 4, 6), (1, 3, 5), (3, 5, 7),
                   (0, 1, 4), (1, 4, 5), (2, 3, 6), (3, 6, 7) ]

        texcrd = [ (0., 0.) ]

        # calibrate
        points = [[a + x, b * z, c + y] for (a, b, c) in points]
        triags = [[a + t, b + t, c + t] for (a, b, c) in triags]
        return points, triags, texcrd

    def _render_walls(self, mask: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        points = []
        triags = []
        texcrd = []
        counter = 0

        with np.nditer(mask, flags=['multi_index']) as mask_iter:
            for x in mask_iter:
                if x == self._wc:
                    h, w = mask_iter.multi_index
                    pt, tr, tx = self._render_single_wall(w, h, self._wh, counter)
                    points.extend(pt)
                    triags.extend(tr)
                    texcrd.extend(tx)
                    counter += len(pt)

        points = np.array(points, dtype=np.float32)
        triags = np.array(triags, dtype=np.uint32)
        texcrd = np.array(texcrd, dtype=np.float32)

        return points, triags, texcrd

    def _render_base(self, mask: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        h, w = mask.shape

        points = np.array([
            [0, 0, 0],
            [w, 0, 0],
            [0, 0, h],
            [w, 0, h],
        ], dtype=np.float32)

        triags = np.array([
            [0, 2, 1],
            [1, 2, 3],
        ], dtype=np.uint32)

        texcrd = np.array([
            [0., 0.],
            [1., 0.],
            [0., 1.],
            [1., 1.],
        ], dtype=np.float32)

        return points, triags, texcrd

    def _colorize(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
        _rgb2roomtype = {
            1: [192,192,224], # closet
            2: [192,255,255], # bathroom
            3: [224,255,192], # livingroom/kitchen
            4: [255,224,128], # bedroom
            5: [255,160, 96], # hall
            6: [255,224,224], # balcony
            7: [224,224,224],
            8: [224,224,128],
        }

        for class_idx, rgb in _rgb2roomtype.items():
            rgb = np.array(rgb, dtype=np.uint8)
            color_mask = (mask == class_idx)
            image[color_mask] += rgb

        return image

    def render(self, image: np.ndarray,
                     mask:  np.ndarray) -> bytes:

        if self._color:
            image = self._colorize(image, mask)

        _, img_encode = cv2.imencode('.png', image)
        img_encode = img_encode.tobytes()

        bpt, btr, btx = self._render_base(mask)
        bbpt = bpt.tobytes()
        bbtr = btr.tobytes()
        bbtx = btx.tobytes()

        wpt, wtr, wtx = self._render_walls(mask)
        bwpt = wpt.tobytes()
        bwtr = wtr.tobytes()
        bwtx = wtx.tobytes()

        model = gltflib.GLTFModel(
            asset=gltflib.Asset(version='2.0'),
            scenes=[
                gltflib.Scene(nodes=[0, 1]),
            ],
            nodes=[
                gltflib.Node(mesh=0),
                gltflib.Node(mesh=1),
            ],
            materials=[
                gltflib.Material(
                    pbrMetallicRoughness=gltflib.PBRMetallicRoughness(
                        baseColorTexture=gltflib.TextureInfo(
                            index=0,
                            texCoord=0,
                        ),
                        baseColorFactor=[1, 1, 1, 1],
                        metallicFactor=0.,
                        roughnessFactor=1.,
                    ),
                ),
            ],
            textures=[
                gltflib.Texture(
                    source=0,
                ),
            ],
            images=[
                gltflib.Image(
                    bufferView=6,
                    mimeType='image/png',
                )
            ],
            meshes=[
                gltflib.Mesh( # walls
                    primitives=[
                        gltflib.Primitive(
                            mode=gltflib.PrimitiveMode.TRIANGLES,
                            indices=0,
                            attributes=gltflib.Attributes(
                                POSITION=1,
                            ),
                        ),
                    ]
                ),
                gltflib.Mesh( # base
                    primitives=[
                        gltflib.Primitive(
                            mode=gltflib.PrimitiveMode.TRIANGLES,
                            indices=3,
                            material=0,
                            attributes=gltflib.Attributes(
                                POSITION=4,
                                TEXCOORD_0=5,
                            ),
                        ),
                    ]
                ),
            ],
            accessors=[
                gltflib.Accessor( # walls triangles
                    bufferView=0,
                    byteOffset=0,
                    count=wtr.size,
                    min=[int(wtr.min())],
                    max=[int(wtr.max())],
                    componentType=gltflib.ComponentType.UNSIGNED_INT.value,
                    type=gltflib.AccessorType.SCALAR.value,
                ),
                gltflib.Accessor( # walls points
                    bufferView=1,
                    byteOffset=0,
                    count=len(wpt),
                    min=wpt.min(axis=0).tolist(),
                    max=wpt.max(axis=0).tolist(),
                    componentType=gltflib.ComponentType.FLOAT.value,
                    type=gltflib.AccessorType.VEC3.value,
                ),
                gltflib.Accessor( # walls tex
                    bufferView=2,
                    byteOffset=0,
                    count=len(wtx),
                    min=wtx.min(axis=0).tolist(),
                    max=wtx.max(axis=0).tolist(),
                    componentType=gltflib.ComponentType.FLOAT.value,
                    type=gltflib.AccessorType.VEC2.value,
                ),

                gltflib.Accessor( # base triangles
                    bufferView=3,
                    byteOffset=0,
                    count=btr.size,
                    min=[int(btr.min())],
                    max=[int(btr.max())],
                    componentType=gltflib.ComponentType.UNSIGNED_INT.value,
                    type=gltflib.AccessorType.SCALAR.value,
                ),
                gltflib.Accessor( # base points
                    bufferView=4,
                    byteOffset=0,
                    count=len(bpt),
                    min=bpt.min(axis=0).tolist(),
                    max=bpt.max(axis=0).tolist(),
                    componentType=gltflib.ComponentType.FLOAT.value,
                    type=gltflib.AccessorType.VEC3.value,
                ),
                gltflib.Accessor( # base tex
                    bufferView=5,
                    byteOffset=0,
                    count=len(btx),
                    min=btx.min(axis=0).tolist(),
                    max=btx.max(axis=0).tolist(),
                    componentType=gltflib.ComponentType.FLOAT.value,
                    type=gltflib.AccessorType.VEC2.value,
                ),
            ],
            bufferViews=[
                gltflib.BufferView( # wall triangles
                    buffer=0,
                    byteOffset=0,
                    byteLength=len(bwtr),
                    target=gltflib.BufferTarget.ARRAY_BUFFER.value,
                ),
                gltflib.BufferView( # wall points
                    buffer=1,
                    byteOffset=0,
                    byteLength=len(bwpt),
                    target=gltflib.BufferTarget.ARRAY_BUFFER.value,
                ),
                gltflib.BufferView( # wall tex
                    buffer=2,
                    byteOffset=0,
                    byteLength=len(bwtx),
                    target=gltflib.BufferTarget.ARRAY_BUFFER.value,
                ),

                gltflib.BufferView( # base triangles
                    buffer=3,
                    byteOffset=0,
                    byteLength=len(bbtr),
                    target=gltflib.BufferTarget.ARRAY_BUFFER.value,
                ),
                gltflib.BufferView( # base points
                    buffer=4,
                    byteOffset=0,
                    byteLength=len(bbpt),
                    target=gltflib.BufferTarget.ARRAY_BUFFER.value,
                ),
                gltflib.BufferView( # base tex
                    buffer=5,
                    byteOffset=0,
                    byteLength=len(bbtx),
                    target=gltflib.BufferTarget.ARRAY_BUFFER.value,
                ),
                gltflib.BufferView( # image
                    buffer=6,
                    byteOffset=0,
                    byteLength=len(img_encode),
                    target=gltflib.BufferTarget.ARRAY_BUFFER.value,
                ),
            ],
            buffers=[
                gltflib.Buffer(
                    uri='bwtr.bin',
                    byteLength=len(bwtr),
                ),
                gltflib.Buffer(
                    uri='bwpt.bin',
                    byteLength=len(bwpt),
                ),
                gltflib.Buffer(
                    uri='bwtx.bin',
                    byteLength=len(bwtx),
                ),
                gltflib.Buffer(
                    uri='bbtr.bin',
                    byteLength=len(bbtr),
                ),
                gltflib.Buffer(
                    uri='bbpt.bin',
                    byteLength=len(bbpt),
                ),
                gltflib.Buffer(
                    uri='bbtx.bin',
                    byteLength=len(bbtx),
                ),
                gltflib.Buffer(
                    uri='img.bin',
                    byteLength=len(img_encode),
                ),
            ],
        )

        gltf = gltflib.GLTF(model=model, resources=[
                gltflib.FileResource('bwtr.bin', data=bwtr),
                gltflib.FileResource('bwpt.bin', data=bwpt),
                gltflib.FileResource('bwtx.bin', data=bwtx),
                gltflib.FileResource('bbtr.bin', data=bbtr),
                gltflib.FileResource('bbpt.bin', data=bbpt),
                gltflib.FileResource('bbtx.bin', data=bbtx),
                gltflib.FileResource('img.bin',  data=img_encode),
            ])

        buffer = io.BytesIO(initial_bytes=b'')
        gltf._embed_buffer_resources()
        gltf._write_glb(buffer)

        return buffer.getvalue()
