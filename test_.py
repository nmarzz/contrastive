
import torch
import argparse
import pytest

from data_processing.contrastive_data import ContrastiveData

''' Install pytest - navigate to this directory - call pytest - pray nothing broke'''

parser = argparse.ArgumentParser(description='Constrastive Learning Experiment')
parser.add_argument('--batch-size', type=int, default=64, metavar='N',
                    help='input batch size for training (default: 128)')
parser.add_argument('--epochs', type=int, default=10, metavar='N',
                    help='number of epochs to train (default: 10)')
parser.add_argument('--lr', type=float, default=0.1, metavar='LR',
                    help='learning rate (default: 0.1)')
parser.add_argument('--dropout', type=float, default=0.25, metavar='P',
                    help='dropout probability (default: 0.25)')
parser.add_argument('--momentum', type=float, default=0.9, metavar='M',
                    help='heavy ball momentum in gradient descent (default: 0.9)')
parser.add_argument('--frac-labeled', type=float, default=0.99, metavar='FL',
                    help='Fraction of labeled data (default 0.99))')
parser.add_argument('--data-dir', type=str, default='./data',metavar='DIR')
args = parser.parse_args()
args.cuda =  torch.cuda.is_available()
kwargs = {'num_workers': 1, 'pin_memory': True} if args.cuda else {}



''' Testing functions below here '''

def test_labelsStripped():
    '''If the labels are stripped, the first element '''
    dataLoaders = ContrastiveData(args, **kwargs).get_data_loaders()
    test= iter(dataLoaders['unlabeled'])
    assert (type(next(test)) is not list), 'The labels were not stripped off'

def test_badData():
    with pytest.raises(ValueError) as context:
        dataLoaders = ContrastiveData(args,dataset_name = '!@##$$)*^!^@##@****!!@GDTGENOTADATASET', **kwargs)
    assert  "Dataset name is not supported" in str(context)
