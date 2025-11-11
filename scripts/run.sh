######## SC ########
python preprocess.py dataset=SC num_workers=50

mkdir -p logs/SC
python train.py dataset=SC cuda=5 > logs/SC/train.log 2>&1 &

python test.py dataset=SC cuda=5 > logs/SC/test.log 2>&1 &

######## IS ########
python preprocess.py dataset=IS num_workers=50

mkdir -p logs/IS
python train.py dataset=IS cuda=5 > logs/IS/train.log 2>&1 &

python test.py dataset=IS cuda=5 > logs/IS/test.log 2>&1 &

######## CA ########
python preprocess.py dataset=CA num_workers=50

mkdir -p logs/CA
python train.py dataset=CA cuda=5 > logs/CA/train.log 2>&1 &

python test.py dataset=CA cuda=5 > logs/CA/test.log 2>&1 &


