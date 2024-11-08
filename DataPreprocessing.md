# Data Preprocessing (for Manual Data Collection Only)


- Original images from the car cameras are **320x160** pixels.

<div align="center">
    <img src="images/3.png" width="320" height="160" />
</div>

- **Data augmentation** to increase the dataset for training:
   1. For center camera images, the steering angle is used as it is.
   2. For left camera images, the steering angle is increased by **0.2**.

<div align="center">
    <img src="images/5.png" width="320" height="160" />
</div>

   3. For right camera images, the steering angle is decreased by **0.2**.

<div align="center">
    <img src="images/6.png" width="320" height="160" />
</div>

   4. **Image augmentation**: Flip the images horizontally and reverse the steering angle sign.

<div align="center">
    <img src="images/11.png" width="320" height="160" />
</div>

   5. Additional augmentations include image translation and brightness adjustments while maintaining the steering angle.

<div align="center">
    <img src="images/8.png" width="320" height="160" />
    <br>
    <em>Add brightness</em>
    <br>
    <br>
    <img src="images/9.png" width="320" height="160" />
    <br>
    <em>Add darkness</em>
    <br>
    <br>
    <img src="images/10.png" width="320" height="160" />
    <br>
    <em>Move</em>
    <br>
    <br>
</div>

<br>
   
This process helps **avoid overfitting**, ensuring that the model generalizes well by having a larger variety of training data.

- **Note**: The car's front and the sky are not important for predicting the steering angle, so they are cropped out.
- Since we are using a CNN, all input images must be resized to the same dimensions, so images are reshaped to **66x200** pixels.

<div align="center">
    <img src="images/12.png" width="200" height="66" />
</div>