# Problem Statement
In this assignment, you will build a complete neural network using Numpy. You will implement all the steps required to build a network - feedforward, loss computation, backpropagation, weight updates etc.

You will use the MNIST dataset to train your model to classify handwritten digits between 0-9.

The assignment is divided into the following sections:
- Data preparation
- Feedforward
- Loss computation
- Backpropagation
- Parameter updates
- Model training and predictions

The following sections walk you through the different sections of the code.

## Data Preparation
You do not have to write any code in this section (Data Preparation). Please refer to the code provided in the notebook while going through these sections.

Firstly, we load the data using the function *load_data()*. The function *data_wrapper()* is then applied to the data to get the train and test data in the desired shape. Please note that the code needs to take a batch of data points as the input. Hence, be careful while checking the dimensions.

You already know that we have 28x28 greyscale images in the MNIST dataset. Hence, each input image is a vector of length 784. The ground truth labels of a batch are stored in a matrix which is converted to a one-hot matrix. Also, the output of the model is a softmax output of length 10. 

Hence, we have the following:
```
train_set_x shape: (784, 50000)
train_set_y shape: (10, 50000)
test_set_x shape: (784, 10000)
test_set_y shape: (10, 10000)
```

Now that the data is in the required shape, let's look at the next section - **feedforward**.

## Feedforward
There are functions assigned to different subparts of feedforward which we will discuss in some time. But before that, there are some things to take into consideration that will help in implementing the code.
- The whole data is taken as one batch. **No minibatch** gradient descent is performed
- The cumulative input to the layer *Z<sup>l</sup>* is now a step in feedforward
- The output of the last layer is denoted as *H<sup>L</sup>* instead of *P* where layer *L* is the final output layer. Hence, there are *L−1* hidden layers.
- For each layer *l*, the *Z<sup>l</sup>* is stored as 'activation_memory' and *H<sup>l−1</sup>, W<sup>l</sup>, b<sup>l</sup>* are stored as 'linear_memory' to use later in backpropagation

You have already studied the feedforward algorithm. Let us summarize it here with respect to the changes mentioned above:
1. *H<sub>0</sub> = B*
2. for *l* in [1,2,.......,*L−1*]:
   1. *Z<sup>l</sup> = W<sup>l</sup>.H<sup>l−1</sup> + b<sup>l</sup>*
   2. *H<sup>l</sup> = σ(Z<sup>l</sup>)*
3. *H<sup>L</sup> = softmax(W<sup>L</sup>.H<sup>L−1</sup> + b<sup>L</sup>)*

Now, let's summarize all the functions we have defined in feedforward:
| Function | Arguments | Returns | Explanation |
|----------|-----------|---------|-------------|
| **sigmoid** | *Z* | *H, sigmoid_memory* | Applies **sigmoid** activation on *Z* to calculate *H*. Returns *H, sigmoid_memory = Z* (Step 2.2) |
| **relu** | *Z* | *H, relu_memory* | Applies **relu** activation on *Z* to calculate *H*. Returns *H, relu_memory = Z* (Step 2.2) |
| **softmax** | *Z* | *H, softmax_memory* | Applies **softmax** activation on *Z*, i.e raise to an exponent and then normalize to get *H*. Returns *H, softmax_memory = Z* (Step 2.2) |
| **initialize_parameters** |	*dimensions* |	*W* and *b* for all the layers |	Runs a for loop to initialize the *W* and *b* of all the layers stored as dictionary *parameters* |
| **layer_forward** | *H_prev, W, b, activation* |	*H, memory* | Performs Step 2. Computes *Z* using step 2.1 and stores *Z* as *linear_memory* and then computes *H, activation_memory* using *Z* as input into the activation functions defined above. Check the arguments and returns of **relu, sigmoid, softmax** to define this function. Returns *H* & *memory = (linear_memory, activation_memory)* |
| **L_layer_forward** |	*X, parameters* |	*HL, memories* | Uses parameters initialized by **initialize_parameters** and performs feedforward using **layer_forward** in a 'for loop' for all layers. Appends *memory* for each layer to *memories*. **layer_forward** for the last layer is performed outside the loop since the activation function for all layers is **relu** except for the last layer (which is **softmax**). Returns the network output *HL* and *memories*. (Steps 1 to 3) |

This should help you in using the functions at the correct places looking at the arguments and the return values. Let's now look at the description of the loss function.

## Loss Calculation
The loss used for multiclass classification is the cross-entropy loss.

| **Function** | **Arguments** |	**Returns** | **Explanation** |
|--------------|---------------|-------------|-----------------|
| **compute_loss** |	*HL, Y* | *loss* | It returns *loss* as the average of the loss of all data points. *HL* and *Y* are matrices. Hence, loss = -1.\*average of the sum of all the elements of the matrix *Ylog(HL)* multiplied element-wise. |

## Backpropagation
The important points to keep in mind are:
- The *parameters* dictionary is getting updated in place at each step.
- The memories from **L_layer_forward** consisting of the tuple *memory = (linear_memory, activation_memory)* for each layer is used in backpropagation
- The backpropagation process will run in a loop from the last layer to the first, and each loop will compute the gradients for 
*Z, H, W, b*.

The backpropagation algorithm pseudocode is as follows:
1. *DZ<sup>L</sup> = P − Y*
2. *<sup>∂L</sup>/<sub>∂W<sup>L</sup></sub> = <sup>1</sup>/<sub>m</sub>DW<sup>L</sup> = <sup>1</sup>/<sub>m</sub>DZ<sup>L</sup>.(H<sup>L−1</sup>)<sup>T</sup>*
3. *<sup>∂L</sup>/<sub>∂b<sup>L</sup></sub> = <sup>1</sup>/<sub>m</sub>Db<sup>L</sup> = <sup>1</sup>/<sub>m</sub>DZ<sup>L</sup>*
4. *dH<sup>L−1</sup> = (W<sup>L</sup>)<sup>T</sup>.DZ<sup>L</sup>*
5. for *l* in *[L−1,........1]*:
   1. *DZ<sup>l</sup> = dH<sup>l</sup>⊗σ′(Z<sup>l</sup>)*
   2. *<sup>∂L</sup>/<sub>∂W<sup>l</sup></sub> = <sup>1</sup>/<sub>m</sub>DW<sup>l</sup> = <sup>1</sup>/<sub>m</sub>DZ<sup>l</sup>.(H<sup>l−1</sup>)<sup>T</sup>*
   3. *<sup>∂L</sup>/<sub>∂b<sup>l</sup></sub> = <sup>1</sup>/<sub>m</sub>Db<sup>l</sup> = <sup>1</sup>/<sub>m</sub>DZ<sup>l</sup>*
   4. *dH<sup>l−1</sup> = (W<sup>l</sup>)<sup>T</sup>.DZ<sup>l</sup>*

Now, let's summarize all the functions we have defined in backpropagation:
| **Functions** |	**Arguments** | **Returns** | **Explanation** |
|---------------|---------------|-------------|-----------------|
| **sigmoid_backward** | *dH, sigmoid_memory* |	*dZ* | *Z = sigmoid_memory* (stored during feedforward); uses this *Z* and *dH* to calculate the gradient *dZ* (Step 5.1) |
| **relu_backward** | *dH, relu_memory* | dZ | *Z = relu_memory* (stored during feedforward); uses this *Z* and *dH* to calculate the gradient *dZ* (Step 5.1) |
| **layer_backward** | *dH, memory, activation* | *dH_prev, dW, db* | Performs Steps 5.1 to 5.4. Calculates *dZ* using activation_backward and then uses *dZ* to calculate *dH_prev, dW, db* using equations in steps 5.2 to 5.4. |
| **L_layer_backward** | *HL, Y, memories* |	*gradients* | Uses **layer_backward** in a 'for loop' using relu activation to get gradients  *dH_prev, dW, db* stored in a dictionary *gradients*. Note that the backprop for the last layer(Steps 1 to 4) is calculated outside and before the for loop. Returns *gradients* which has *dH, dW, db* for all the layers. |

The following image should help you in understanding the workflow:

![feed_forward_backward](feed_forward_backward.png)

## Parameter Updates
In this section, you have to define the function that updates the weights and biases for all the layers using a 'for' loop.
| **Function** | **Arguments** |	**Returns** | **Explanation** |
|--------------|---------------|-------------|-----------------|
| **update_parameters** | *parameters, gradients, learning_rate* | *parameters* | *parameters* has the parameters which is updated using the *learning_rate* and the *gradients* stored in gradients. |

## Model Training
This is the final step in which you combine all the functions created above to define an 'L_layer_model'. 

| **Function** | **Arguments** |	**Returns** | **Explanation** |
|--------------|---------------|-------------|-----------------|
| **L_layer_model** | *X, Y, dimensions, learning_rate , num_iterations, print_loss* |	*parameters* |	Initializes parameters with **initialize_parameters**. In a for loop uses functions **L_layer_forward, compute_loss, L_layer_backward, update_parameters** in the specified order. |

After this, you can start the training by specifying the learning rate and the number of iterations.

### Important Note on Training
The training will take about 10-20 minutes with about 2000 iterations, which is a recommended number to achieve good accuracy (> 75%).

Enjoy making your own neural network!
