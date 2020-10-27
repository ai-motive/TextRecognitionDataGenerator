#!/usr/bin/env bash
conda activate TextRecognitionDataGenerator
source env_setup.sh

round() {
  printf "%.${2}f" "${1}"
}

INPUT_PATH='./texts/korean_texts.txt'
imgH=64
num_imgs=$((37*1))

# Train / Test ratio (8:2)
train_ratio=0.8
test_ratio=$(echo "1 - $train_ratio" | bc -l)

train_basic_cnt=$(round $(echo "$num_imgs * $train_ratio" | bc -l) 0)
test_basic_cnt=$(round $(echo "$num_imgs * $test_ratio" | bc -l) 0)

train_skew_cnt=$train_basic_cnt
test_skew_cnt=$test_basic_cnt

train_dist_cnt=0 # 스캔 문서에는 왜곡이 거의 없음
test_dist_cnt=0

train_blur_cnt=$train_basic_cnt
test_blur_cnt=$test_basic_cnt

train_gaussian_cnt=$train_basic_cnt
test_gaussian_cnt=$test_basic_cnt

train_custom_cnt=$train_basic_cnt
test_custom_cnt=$test_basic_cnt

train_total_cnt=$(($train_basic_cnt+$train_skew_cnt+$train_dist_cnt+$train_blur_cnt+$train_gaussian_cnt+$train_custom_cnt))
test_total_cnt=$(($test_basic_cnt+$test_skew_cnt+$test_dist_cnt+$test_blur_cnt+$test_gaussian_cnt+$test_custom_cnt))
total_cnt=$(($train_total_cnt+$test_total_cnt))
printf "[TRAIN] Train total images : %s\n" $train_total_cnt
printf "[TEST] Test total images : %s\n" $test_total_cnt
printf "[TOTAL] Total images : %s\n" $total_cnt

# [Basic images] -> (num_fonts(11) * num_text_sequences(4))
python run_custom.py \
  --output_dir out/ko/train/basic --input_file $INPUT_PATH  --language ko --count $train_basic_cnt \
  --format $imgH --background 1 --name_format 2 --margins 0,0,0,0 --fit \
  --font_dir ./fonts/ko/
printf "[TRAIN] Basic images generated : %s\n" $train_basic_cnt
python run_custom.py \
  --output_dir out/ko/test/basic --input_file $INPUT_PATH  --language ko --count $test_basic_cnt \
  --format $imgH --background 1 --name_format 2 --margins 0,0,0,0 --fit \
  --font_dir ./fonts/ko/
printf "[TEST] Basic images generated : %s\n" $test_basic_cnt

# [Skew images] -> (num_fonts(11) * num_text_sequences(4))
python run_custom.py \
  --output_dir out/ko/train/skew --input_file $INPUT_PATH --language ko --count $train_skew_cnt \
  --format $imgH --skew_angle 2 --random_skew --background 1 \
  --name_format 2 --margins 0,0,0,0 --fit --font_dir ./fonts/ko/
printf "[TRAIN] Skew images generated : %s\n" $train_skew_cnt
python run_custom.py \
  --output_dir out/ko/test/skew --input_file $INPUT_PATH --language ko --count $test_skew_cnt \
  --format $imgH --skew_angle 2 --random_skew --background 1 \
  --name_format 2 --margins 0,0,0,0 --fit --font_dir ./fonts/ko/
printf "[TEST] Skew images generated : %s\n" $test_skew_cnt

#    ## 스캔 문서에는 왜곡이 거의 없음
## [Dist.] -> (num_fonts(11) * num_text_sequences(4))
#    python run_custom.py \
#      --output_dir out/ko/train/dist --input_file $INPUT_PATH --language ko --count $train_dist_cnt \
#      --format $imgH --distorsion 3 --distorsion_orientation 2 --background 1 \
#      --name_format 2 --margins 0,0,0,0 --fit --font_dir ./fonts/ko/
# printf "[TRAIN] Dist. images generated : %s\n" $train_dist_cnt
#    python run_custom.py \
#      --output_dir out/ko/test/dist --input_file $INPUT_PATH --language ko --count $test_dist_cnt \
#      --format $imgH --distorsion 3 --distorsion_orientation 2 --background 1 \
#      --name_format 2 --margins 0,0,0,0 --fit --font_dir ./fonts/ko/
# printf "[TEST] Dist. images generated : %s\n" $test_dist_cnt

## [Blur Images] -> (num_fonts(11) * num_text_sequences(4))
python run_custom.py \
  --output_dir out/ko/train/blur --input_file $INPUT_PATH --language ko --count $train_blur_cnt \
  --format $imgH --blur 1 --random_blur --background 1 \
  --name_format 2 --margins 0,0,0,0 --fit --font_dir ./fonts/ko/
printf "[TRAIN] Blur images generated : %s\n" $train_blur_cnt
python run_custom.py \
  --output_dir out/ko/test/blur --input_file $INPUT_PATH --language ko --count $test_blur_cnt \
  --format $imgH --blur 1 --random_blur --background 1 \
  --name_format 2 --margins 0,0,0,0 --fit --font_dir ./fonts/ko/
printf "[TEST] Blur images generated : %s\n" $test_blur_cnt

# [Gaussian Images] -> (num_fonts(11) * num_text_sequences(4))
# Gaussian noise
python run_custom.py \
  --output_dir out/ko/train/back --input_file $INPUT_PATH --language ko --count $train_gaussian_cnt \
  --format $imgH --background 0 \
  --name_format 2 --margins 0,0,0,0 --fit --font_dir ./fonts/ko/
printf "[TRAIN] Gaussian noise images generated : %s\n" $train_gaussian_cnt
python run_custom.py \
  --output_dir out/ko/test/back --input_file $INPUT_PATH --language ko --count $test_gaussian_cnt \
  --format $imgH --background 0 \
  --name_format 2 --margins 0,0,0,0 --fit --font_dir ./fonts/ko/
printf "[TEST] Gaussian noise images generated : %s\n" $test_gaussian_cnt

# [Custom background images] -> (num_fonts(11) * num_text_sequences(4))
python run_custom.py \
  --output_dir out/ko/train/back --input_file $INPUT_PATH --language ko --count $train_custom_cnt \
  --format $imgH --background 3 \
  --name_format 2 --margins 0,0,0,0 --fit --font_dir ./fonts/ko/
printf "[TRAIN] Custom background images generated : %s\n" $train_custom_cnt
python run_custom.py \
  --output_dir out/ko/test/back --input_file $INPUT_PATH --language ko --count $test_custom_cnt \
  --format $imgH --background 3 \
  --name_format 2 --margins 0,0,0,0 --fit --font_dir ./fonts/ko/
printf "[TEST] Custom background images generated : %s\n" $test_custom_cnt

printf "[TRAIN] Total images generated : %s\n" $train_total_cnt
printf "[TEST] Total images generated : %s\n" $test_total_cnt
printf "[TOTAL] Total images generated : %s\n" $total_cnt

