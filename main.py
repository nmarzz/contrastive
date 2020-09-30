import torch
import argparse
import matplotlib.pyplot as plot
from data_processing.contrastive_data import ContrastiveData
import torch.nn as nn
import torch.optim as optim
import torchnet as tnt

# Parse arguments
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
parser.add_argument('--frac-labeled', type=float, default=0.01, metavar='FL',
                    help='Fraction of labeled data (default 0.01))')
parser.add_argument('--data-dir', type=str, default='./data',metavar='DIR')
args = parser.parse_args()
args.cuda =  torch.cuda.is_available()

# Print out arguments to the log
print('Constrastive Learning Run')
for p in vars(args).items():
    print('  ',p[0]+': ',p[1])
print('\n')

kwargs = {'num_workers': 1, 'pin_memory': True} if args.cuda else {}

def returnClosestCenter(centers,points):
    ''' Returns the value of the center closest to each point
        - input
    '''
    # thank you pytorch for excellent indexing abilities
    distance = torch.cdist(centers,points)
    m,indicies = torch.min(distance,0)
    closest = centers[indicies,:]
    closest.requires_grad = True
    return closest

### Let's define the simplest network I can
class SimpleNet(nn.Module): #  With Projection data we should see the identity map from R^n to R^N/2

    def __init__(self,num_clusters):
        super(SimpleNet,self).__init__()
        self.num_clusters = num_clusters
        self.net = nn.Sequential(
            nn.Linear(2*num_clusters,2*num_clusters)
        )

    def forward(self,x): # No activation function, just one map of weights.
        return self.net(x)

def distanceLoss(labeled_ouput,labeled_centers):
    return torch.sum((labeled_ouput - labeled_centers)**2)


num_clusters = 2
eye = torch.eye(2*num_clusters,2*num_clusters)
centers = eye[0:num_clusters,:]

data = ContrastiveData(args.batch_size,args.frac_labeled,args.data_dir,dataset_name = 'Projection',num_clusters = num_clusters, **kwargs)
data_loaders = data.get_data_loaders()

model = SimpleNet(num_clusters)
optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum = args.momentum)

if args.cuda:
    model.cuda()

def train(epoch):
    model.train()
    # Train on labeled data first
    for batch_ix, (data, target) in enumerate(data_loaders['labeled']):
        if args.cuda:
            data, target = data.cuda(), target.cuda()

        optimizer.zero_grad()
        output = model(data)
        loss = distanceLoss(output, target)
        loss.backward()
        optimizer.step()
        if batch_ix % 100 == 0 and batch_ix>0:
            print('[Epoch %2d, batch %3d] training loss: %.4f' %
                (epoch, batch_ix, loss.data[0]))

    for batch_ix,(data) in enumerate(data_loaders['unlabeled']):
        if args.cuda:
            data= data.cuda()
        optimizer.zero_grad()
        output = model(data)
        loss = distanceLoss(data,returnClosestCenter(centers,data))
        loss.backward()
        optimizer.step()


def test():
    model.eval()
    test_loss = tnt.meter.AverageValueMeter()
    top1 = tnt.meter.ClassErrorMeter()
    with torch.no_grad():
        for data, target in data_loaders['test']:
            if args.cuda:
                data, target = data.cuda(), target.cuda()
            output = model(data)
            loss = distanceLoss(output, target)
            print(loss)

if __name__=="__main__":
    for epoch in range(1, args.epochs + 1):
        train(epoch)
        test()
