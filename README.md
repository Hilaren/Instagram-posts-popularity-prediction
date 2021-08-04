**Motivation**

Over the past decade, social media has become a most important marketing strategy, no matter you own a small local shop or a big international company, it offers great opportunities for business growth, branding awareness, and customer relationship building. 

I've been working in the online ads industry for a few years. Working as a consultant, I help thousands of marketers to analyze the campaigns' performance, the creatives' popularity, and so forth. Based on my experience, generating the most attractive creatives has always been the biggest challenge for most marketers, generally, it takes at least a week for marketers to tell the performance of a newly launched post until a clear insight is available. 

In this situation, a predictive tool that can predict the post engagement rates before it's being launched would be budget-saving and efficient.

During unpack AI Bootcamp 101, I've learned fastai vision model which seems could be an appropriate approach to solve the issue above.

In this article, I chose Sezane posts from Instagram to validate my machine learning model. I will show you:

1. The approach I attempted to predict the popularity of an Instagram image using fastai Vision Model;
2. Results of the model, actually I failed;
3. Conclusions and learnings;

**Popularity Prediction Model**

**Step1: Building the dataset.**

The biggest challenge associated with this project is data collecting. Instagram provides 2 APIs for data exporting:

Instagram Basic Display API allows users of your app to get basic profile information, photos, and videos in their Instagram accounts.

Instagram Graph API allows Instagram Professionals - Businesses and Creators - to use the app to manage their presence on Instagram.
Apparently, none of the above is available to the public domain, thus couldn't be used for this project, I also tried some other approaches to crawl the data while failed. 

Eventually, I decided to download photos along with the number of Likes and the number of Comments manually. It took me around 7 hours totally to collect around 500 images from the Sezane account.

**Step2: Analyzing and cleaning the dataset**

Cleaning the dataset is also a challenging step.

With Instagram ads, the advertisers can advertise a specific image or video which can drive more engagement accordingly. By checking the number of Likes and Comments of hundreds of images under the Sezane account, I found that the ratio of Likes-Comments for non-advertised images is likely between 0.5% and 2%, also the number of Likes more than 16,000 are likely to be an advertised post. 

Below is calculated with the original, uncleaned dataset, we can see a high standard deviation from the table, the mean is 10,594 (take numberLikes as an example) while 60% of the images have less than the mean number. Apparently, the issue was caused by advertised images, the following graph also confirms the values shown on the table.

I did the following actions to remove the advertised images:

1. Only keep the images with a Comment-Like ratio between 0.5% and 2%.
2. Remove the images with the number of Likes over 16,000.

After filtering, the standard deviation went down as below.
1. numberLikes: 6085 → 2897;
2. numberComments: 98 → 44;

Dataset and Segmentations: (Total = NumberLikes+NumberComments)
The dataset was roughly segmented into 3 classes:
1. Low Engagement (107 images): Total < 7,000
2. Neutral (142 images) : 7,000 < Total < 11,000
3. High Engagement (95 images) : Total > 11,000

Note: Total = numberLikes + numberComments

**Step 3: Learning Model and Accuracy**

I'm using fastai vision model to create this model, the model, for now, doesn't work as the accuracy is only around 40%, I will keep training the model by adding more data and using different data augmentation and keep updating the code in Github. Also, you could play it using this build-in web App.

1. Conclusion on data augmentation: Data augmentation should be used.

2. Conclusion on architectures: resnet 34 works the best.

3. Increase epochs with resnet34: overfitting when epochs more than 3.

**Step4: Final Result with the test dataset**

This image above has 15,100 Likes and 263 Comments, based on the baseline I set up, it should be High Engagement, while the model predicted it as Neutral which is incorrect. I tested the model with around 20 images and just got around 50% accuracy which is aligned with the accuracy rate showed in the previous part.

**Conclusions and Learnings**

From the results shown above, I would say fastai vision model could probably be used to predict the popularity of Instagram posts if the following items being taken into consideration when building the model.

1. More images should be added. 100 images for each class is way little for training such a complicated model. At least 3,000 images for each class were suggested by a seasoned AI practitioner. 

2. More factors should be considered when segmenting the classes. The classes, namely the engagement levels(High/Neutral/Low) I defined was just simply using the number of Likes/Comments which is apparently not enough. The posts' performance on social media could be impacted by a lot of various factors, such as posting time, labels attached, advertised or not, and so forth. 

3. Rethink on the grouping. I roughly defined the sum of the number of Likes and Comments below 7,000 as Low Engaged and the ones with over 11,000 as High Engaged, apparently this grouping method is too rough and not accurate. 

4. Try fastai tabular model. 

Predicting the popularity of a social media post is tough, but it's interesting, isn't it?
