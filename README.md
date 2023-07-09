# WAVY

## What is wavy?

Wavy is a simple api written with python and flask which creates beautiful SVG waves. Useful for backgrounds, headers, etc.

## Endpoints

### /api/wave

Default endpoint for creating a wave.

#### Parameters

| Parameter      | Type    | Description                                                     | Default  |
| -------------- | ------- | --------------------------------------------------------------- | -------- |
| `width`        | `int`   | The width of the wave                                           | `1920`   |
| `height`       | `int`   | The height of the wave                                          | `1080`   |
| `color`        | `str`   | The color of the wave                                           | `78fa67` |
| `start`        | `float` | The start of the wave (between 0 and 1)                         | `0.4`    |
| `wonkyness`    | `int`   | The wonkyness of the wave                                       | `4`      |
| `points`       | `int`   | The amount of points in the wave                                | `5`      |
| `resolution`   | `int`   | The resolution of the wave, i.e. line-segment count             | `100`    |
| `only_include` | `str`   | The only values to return. Example: "path", "color", "width"... | `None`   |

#### Disclamer

If no `only_include` parameter is given, the api will return the full svg. If you only want the path, you can use the `only_include` parameter to only return the actual path.

### /api/waves

Endpoint for creating multiple waves at the same time. Option to seamlessly go from one color for the first wave to another for the last wave. Has the same parameters as `/api/wave` but with the following additional parameters.

#### Parameters

| Parameter     | Type    | Description                   | Default  |
| ------------- | ------- | ----------------------------- | -------- |
| `layers`      | `int`   | The amount of waves to create | `6`      |
| `start_color` | `str`   | The start color of the waves  | `e7233a` |
| `end_color`   | `str`   | The end color of the waves    | `01051e` |
| `start_y`     | `float` | The start y of the waves      | `0.2`    |
| `end_y`       | `float` | The end y of the waves        | `0.5`    |

## Examples

Reload to see new waves.

### /api/wave

Params: [`width=1920&height=1080&color=00ffff&start=0.4&wonkyness=4&points=5&resolution=100`](https://wavy-runarmod.vercel.app/api/wave?width=1920&height=1080&color=00ffff&start=0.4&wonkyness=4&points=5&resolution=100)

![/api/wave](https://wavy-runarmod.vercel.app/api/wave?width=1920&height=1080&color=00ffff&start=0.4&wonkyness=4&points=5&resolution=100)

Params: [`width=1920&height=1080&color=78fa67&start=0.4&wonkyness=4&points=5&resolution=6`](https://wavy-runarmod.vercel.app/api/width=1920&height=1080&color=78fa67&start=0.4&wonkyness=4&points=5&resolution=6)

![/api/wave](https://wavy-runarmod.vercel.app/api/wave?width=1920&height=1080&color=78fa67&start=0.4&wonkyness=4&points=5&resolution=6)

Params: [`width=1920&height=1080&color=e7233a&start=0.7&wonkyness=8&points=8`](https://wavy-runarmod.vercel.app/api/width=1920&height=1080&color=e7233a&start=0.7&wonkyness=8&points=8)

![/api/wave](https://wavy-runarmod.vercel.app/api/wave?width=1920&height=1080&color=e7233a&start=0.7&wonkyness=8&points=8)

Params: [`color=777&points=100&resolution=500&wonkyness=10`](https://wavy-runarmod.vercel.app/api/color=777&points=100&resolution=500&wonkyness=10)

![/api/wave](https://wavy-runarmod.vercel.app/api/wave?color=777&points=100&resolution=500&wonkyness=10)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
