## Usage
## Staging:
## ssh tzcld-stg@astral.startinblox.com 'bash -s' < deploy.sh
## Production:
## ssh tzcld@astral.startinblox.com 'bash -s' < deploy.sh

cd startinblox
source venv/bin/activate
pip install -U djangoldp djangoldp_account djangoldp_tzcld djangoldp_notification djangoldp_circle djangoldp_communities
cd sibserver
djangoldp configure
cd ../client
git checkout issue-1091
git pull
npm run build

