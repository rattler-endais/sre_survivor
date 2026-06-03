# Sugerencia betatester 02.06.2026. Problemas con el audio al ejecutarlo en WSL
import os
# Engañamos a SDL para que use un driver de audio virtual (ficticio)
# La variable de entorno se debe setear antes de inicializar pygame
# “Do not use a real audio device. Use a fake audio driver instead.”
# This can be useful in environments where audio does not work correctly,
# such as some WSL setups, CI environments, servers, or headless systems.
os.environ["SDL_AUDIODRIVER"] = "dummy"

import sre_survivor.sre_survivor
