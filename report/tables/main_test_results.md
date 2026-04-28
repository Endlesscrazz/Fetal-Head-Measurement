| experiment | run_id | model | loss | augmentation | image_size | base_channels | epochs | split_id | mean_dice | mean_iou | mean_hd95_mm | mae_hc_mm | rmse_hc_mm |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Attention U-Net + BCE/Dice | attention_unet_local_baseline | attention_unet | bce_dice | False | 256x384 | 16 | 10 | seed42_train698_val152_test149 | 0.9669 | 0.9373 | 2.3779 | 3.3690 | 4.6767 |
| Attention U-Net + Dice | attention_unet_dice_loss | attention_unet | dice | False | 256x384 | 16 | 10 | seed42_train698_val152_test149 | 0.9615 | 0.9293 | 2.4840 | 3.4548 | 5.1310 |
| Attention U-Net + BCE/Dice + Aug | attention_unet_aug | attention_unet | bce_dice | True | 256x384 | 16 | 10 | seed42_train698_val152_test149 | 0.9606 | 0.9275 | 2.8276 | 3.7177 | 5.8491 |
| U-Net + BCE/Dice | unet_local_baseline | unet | bce_dice | False | 256x384 | 16 | 10 | seed42_train698_val152_test149 | 0.9600 | 0.9261 | 3.0243 | 3.7794 | 5.5603 |
