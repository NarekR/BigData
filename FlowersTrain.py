import torch
import torch.nn as nn
import torch.optim as optim
from collections import OrderedDict
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader

data_dir = 'C:/Users/Guest_user/Desktop/Flowers'
train_dir = data_dir + '/train'
valid_dir = data_dir + '/valid'
test_dir = data_dir + '/test'

# Define data transforms
train_transforms = transforms.Compose([transforms.RandomRotation(30),
                                       transforms.RandomResizedCrop(224),
                                       transforms.RandomHorizontalFlip(),
                                       transforms.ToTensor(),
                                       transforms.Normalize([0.485, 0.456, 0.406],
                                                            [0.229, 0.224, 0.225])])

valid_transforms = transforms.Compose([transforms.Resize(256),
                                      transforms.CenterCrop(224),
                                      transforms.ToTensor(),
                                      transforms.Normalize([0.485, 0.456, 0.406],
                                                           [0.229, 0.224, 0.225])])
test_transforms = transforms.Compose([transforms.Resize(256),
                                      transforms.CenterCrop(224),
                                      transforms.ToTensor(),
                                      transforms.Normalize([0.485, 0.456, 0.406],
                                                           [0.229, 0.224, 0.225])])


train_data = datasets.ImageFolder(train_dir, transform=train_transforms)
valid_data = datasets.ImageFolder(valid_dir, transform=valid_transforms)
test_data = datasets.ImageFolder(test_dir, transform=test_transforms)

trainloader = torch.utils.data.DataLoader(train_data, batch_size=50, shuffle=True)
validloader = torch.utils.data.DataLoader(valid_data, batch_size=50)
testloader = torch.utils.data.DataLoader(test_data, batch_size=50)

# Load the datasets with ImageFolder
#image_datasets = {x: datasets.ImageFolder(root=f'{data_dir}/{x}', transform=data_transforms[x])
#                  for x in ['train', 'val']}

# Create data loaders
#dataloaders = {x: DataLoader(image_datasets[x], batch_size=4, shuffle=True, num_workers=4)
#               for x in ['train', 'val']}
# Load the pre-trained VGG16 model
model = models.vgg16(pretrained=True)
model.name = "vgg16"
model
# Modify the classifier part of the VGG16 model
num_features = model.classifier[0].in_features
model.classifier = nn.Sequential(
    nn.Linear(num_features, 4096),
    nn.ReLU(inplace=True),
    nn.Dropout(0.5),
    nn.Linear(4096, 4096),
    nn.ReLU(inplace=True),
    nn.Dropout(0.5),
    nn.Linear(4096, 102)  # Change 102 to the number of classes in the Oxford 102 dataset
)
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

# Freeze parameters so we don't backprop through them
for param in model.parameters():
    param.requires_grad = False

# Define a new, untrainted feed-forward network as a classifier, using ReLU activations and dropout
classifier = nn.Sequential(OrderedDict([
    ('fc1', nn.Linear(25088, 4096, bias=True)),
    ('relu1', nn.ReLU()),
    ('dropout1', nn.Dropout(p=0.5)),
    ('fc2', nn.Linear(4096, 102, bias=True)),
    ('output', nn.LogSoftmax(dim=1))
]))

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device);

# Define loss and optimizer
criterion = nn.NLLLoss()
optimizer = optim.Adam(model.classifier.parameters(), lr=0.001)

# Define deep learning method
epochs = 5
print_every = 30 # Prints every 30 images out of batch of 50 images
steps = 0
model.classifier = classifier


# Implement a function for the validation pass
def validation(model,  criterion):
    test_loss = 0
    accuracy = 0

    for ii, (inputs, labels) in enumerate(testloader):
        inputs, labels = inputs.to(device), labels.to(device)

        output = model.forward(inputs)
        test_loss += criterion(output, labels).item()

        ps = torch.exp(output)
        equality = (labels.data == ps.max(dim=1)[1])
        accuracy += equality.type(torch.FloatTensor).mean()

    return test_loss, accuracy
# Train the classifier layers using backpropogation using the pre-trained network to get features

print("Training process initializing .....\n")

for e in range(epochs):
    running_loss = 0
    model.train()  # Technically not necessary, setting this for good measure

    for ii, (inputs, labels) in enumerate(trainloader):
        steps += 1

        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()

        # Forward and backward passes
        outputs = model.forward(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

        if steps % print_every == 0:
            model.eval()

            with torch.no_grad():
                valid_loss, accuracy = validation(model, criterion)

            print("Epoch: {}/{} | ".format(e + 1, epochs),
                  "Training Loss: {:.4f} | ".format(running_loss / print_every),
                  "Validation Loss: {:.4f} | ".format(valid_loss / len(testloader)),
                  "Validation Accuracy: {:.4f}".format(accuracy / len(testloader)))

            running_loss = 0
            model.train()

print("\nTraining process is now complete!!")

