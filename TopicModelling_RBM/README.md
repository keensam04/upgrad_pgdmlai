# Problem Statement
In this assignment, you will train a **Restricted Boltzmann Machine** to perform **Topic Modelling** on a set of Amazon reviews. 

Topic Modelling is the art and science of identifying the 'latent topics' in a text. It is an unsupervised problem. You input a set of documents/ corpus into the model and the model finds the topics that describe the corpus. Each topic is a distribution over the words that best describe the topic. 

 

Let's understand this with the help of an example:

Suppose you are given reviews about a product, for example, iPhone. You can perform topic modelling to see what topics are the people in the reviews talking about. Consider that we have input to the model that we want 3 top topics from the reviews.

The top 5 words that describe the topics are shown below:
| Topic 1 | Topic 2 | Topic 3 |
|---------|---------|---------|
| pixel | smooth | slow |
| selfie | apps | memory |
| good | hangs | storage |
|blur | interface | full |
| filter | intelligent | apps|

Looking at the above words, we can say that Topic 1 mostly talks about the camera of iPhone while Topic 2 talks about the iOS operating system and Topic 3 talks about the storage memory available. It might often happen that you might not be able to figure out the topics from the distribution of the words.

After getting the topics, you can do a lot of things like:
1. Find the distribution of each review over the topics
2. Couple the topics and sentiments of each review and see which topics more often in negative reviews
3. Use the topic representation of each document as a feature representation for developing further machine learning models 

You can use different models to perform topic modelling, one of which is LDA  which you have studied earlier in the Natural Language Processing course.

In this assignment, we will use a Restricted Boltzmann Machine (RBM) to perform topic modelling. The input to an RBM is a bag of words model and the output is the distribution of words in the topics.

The motivation behind studying RBMs is that these are building blocks of **Deep Belief Networks**, a generative class of models which have become quite popular lately.

The training process is contrastive divergence. In this assignment, we shall create a function to perform Gibbs sampling k times within contrastive divergence often referred to as CD-k. Let's understand the structure of the notebook and the CD-k training process:
- Importing the dataset.
- Create a bag of words model.

  Note that the shape of a bag of words model will be (data_size, vocablury_size)
  
  Please **note** that the above shape might vary with the way you perform bag of words model but the index *data_size* will be the same.
- Training using CD-k
  
  This involves performing Gibbs sampling k-times which can be better understood using the following image.

![contrastive_divergence](contrastive_divergence.png)

**<p align=center>Contrastive Divergence</p>**

1. You start with the input batch of data, *v<sub>0</sub>*.
2. You then calculate *p(h|v<sub>0</sub>) = σ(c<sub>j</sub>+∑<sup>n</sup><sub>i=1</sub>v<sub>i</sub>w<sub>ij</sub>)*.

   Vectorized implementation: *p(h|v<sub>0</sub>) = σ(C+V.W)*
3. Using this p(h|v<sub>0</sub>), you sample h<sub>0</sub>.
4. Now that you have got h<sub>0</sub>, you calculate *p(v|h<sub>0</sub>) = σ(b<sub>j</sub>+∑<sup>m</sup><sub>j=1</sub>h<sub>j</sub>w<sub>ij</sub>)*.

   Vectorized implementation: *p(v|h<sub>0</sub>) = σ(B+H.W<sup>T</sup>)*
5. Using this *p(v|h<sub>0</sub>)*, you sample *v<sub>1</sub>*.

You repeat this k times till you get *h<sub>k</sub>* and *v<sub>k</sub>*.

Step 2 and 3 are performed in the function *sampleHiddenLayer()* while Step 4 and 5 are performed in *sampleVisibleLayer()*.

*sampleHiddenLayer()* and *sampleVisibleLayer()* are combined to create a function *gibbs()* which does one iteration of Gibbs sampling.

*gibbs* is repeated k-times in the function *cd_k()* to perform Contrastive Divergence k-times.


You have already learned that the training process in an RBM involves maximizing the joint probability distribution. Using the energy function as defined in the lectures and the above sampling process, the update matrices and vectors simplify as follows:
1. *ΔW = v<sub>0</sub>⊗p(h<sub>0</sub>|v<sub>0</sub>) − v<sub>k</sub>⊗p(h<sub>k</sub>|v<sub>k</sub>)*
2. *Δb = avg_across_batch(v<sub>o</sub>−v<sub>k</sub>)*
3. *Δc = avg_across_batch(p(h<sub>0</sub>|v<sub>o</sub>) − p(h<sub>k</sub>|v<sub>k</sub>))*
You do average across batch because you need a vector update for the bias vectors and *v<sub>o</sub>, v<sub>k</sub>* and *p(h<sub>0</sub>|v<sub>o</sub>), p(h<sub>k</sub>|v<sub>k</sub>)* are matrices.

Since you have to maximize the joint probability distribution, you use **gradient ascent** here with momentum. It is recommended that you understand the working of momentum.

The momentum equations are as follows:
1. *mW<sub>t</sub> = γ mW<sub>t−1</sub> − ΔW*
2. *mb<sub>t</sub> = γ mb<sub>t−1</sub> − Δb*
3. *mc<sub>t</sub> = γ mc<sub>t−1</sub> − Δc*

*γ* is the momentum coefficient here.

Using these momentum terms, you update the weights and biases as follows:
1. *W<sub>t</sub> = W<sub>t−1</sub> + α mW<sub>t</sub>*
2. *b<sub>t</sub> = b<sub>t−1</sub> + α mb<sub>t</sub>*
3. *c<sub>t</sub> = c<sub>t−1</sub> + α mc<sub>t</sub>*

*α* is the learning rate.

The above equations are implemented in the function *train()*.

These equations should help you in implementing topic modelling using RBMs without any issue.

In the end, you'll be able to see the words that constitute the different topics.

All the best!
