#!/bin/bash
python3 -m venv pyenv
echo -e "#!/usr/bin/env bash\nsource ./pyenv/bin/activate" >> ./pyenv.sh
echo -e "#!/bin/bash\npip3 freeze  > requirements.txt" >> ./update_requirments.sh
