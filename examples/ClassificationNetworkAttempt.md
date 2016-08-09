# My Attempt of a Classification Netwrok using DSSTNE
### WORK IN PROGRESS

## Getting the Data
A nice and simple example of a multiclass classification problem is the the iris dataset. The iris dataset is a csv with 5 columns.

1. sepal length in cm
2. sepal width in cm
3. petal length in cm
4. petal width in cm
5. class: (Iris Setosa, Iris Versicolour, Iris Virginica)

Grab the dataset.

```bash
wget https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data
```

Add colume headers by inserting a line into the beginning of the file.

```bash
sed -i '1s/^/sepalLength,sepalWidth,petalLength,petalWidth,class\n/' iris.data
```

## Convert the Data
Now we need to convert the data into a format DSSTNE can read. csvToDsstne.py is a quick script that creates 4 files.

'input.dsstne' and 'output.dsstne' are the files used to train the network.
'test.dsstne' and 'truth.dsstne' are the files used to evaluate the precision/recall of the network.

Run the script.

```bash
python csvToDsstne.py iris.data --label class
```

## Config 
### Again, this is NOT working currently. This is just my attempt so far.
Save the following as **config_iris.json**

```bash
{
	"Version": 0.7,
    "Name" : "Iris",
    "Kind" : "FeedForward",

    "ShuffleIndices" : true,

    "Layers" : [
        { "Name" : "Input", "Kind" : "Input", "N" : "auto", "DataSet" : "gl_input", "Sparse" : true },
        { "Name" : "Hidden1", "Kind" : "Hidden", "Type" : "FullyConnected", "N" : 4, "Activation" : "Sigmoid", "Sparse" : false },
        { "Name" : "Hidden2", "Kind" : "Hidden", "Type" : "FullyConnected", "N" : 3, "Activation" : "Sigmoid", "Sparse" : false },
        { "Name" : "Output", "Kind" : "Output", "Type" : "FullyConnected", "DataSet" : "gl_output", "N" : "auto", "Activation" : "Sigmoid", "Sparse" : true }
    ],

    "ErrorFunction" : "ScaledMarginalCrossEntropy"
}
```

## Generating NC files using Dsstne

Generate input for training.

```bash
generateNetCDF -d gl_input -i input.dsstne -o gl_input.nc -f features_input -s samples_input -c -t analog
```

Generate output for training.

```bash
generateNetCDF -d gl_output -i output.dsstne -o gl_output.nc -f features_output -s samples_input -c -t analog
```

### You can use the following command to view the .nc files dsstne generates if you are curious as to what it looks like.
```bash
ncdump gl_input.nc
```

## Train

```bash
train -c config_iris.json -i gl_input.nc -o gl_output.nc -n gl.nc -b 16 -e 100
```

## Predict

```bash
predict -b 1024 -d gl -i features_input -o features_output -n gl.nc -f test.dsstne -s predictions -r test.dsstne
```

## Evaluate

Predictions are stored in a file called 'predictions' as specified in the predict command. To evaluate the accuracy of the model use reviewResults.py

```bash
reviewResults.py predictions truth.dsstne
```
