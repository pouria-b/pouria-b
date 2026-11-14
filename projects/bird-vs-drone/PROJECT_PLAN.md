# Bird vs. Drone — Original Project Plan

This is a project-focused Markdown transcription of **Pooria_Project**, retrieved from Google Drive on 14 November 2026.

[Source Google Doc](https://docs.google.com/document/d/1wYa8DE7AaLTvF_ujLca8BVgFV2qilFuen8gebzTAkTU)

**Status:** this is an early planning document, not a completed experiment report. Its proposed classification baseline and model comparisons should not be confused with the later YOLO detection project described in the portfolio. Roadmap items below are plans, not verified completed work.

## Description

“In this project, we want to train a classifier to identify birds vs drones.”

Dataset specified in the source:
[Bird vs Drone, by stealthknight on Kaggle](https://www.kaggle.com/datasets/stealthknight/bird-vs-drone).

## Planned report sections

The source includes these headings, with little or no detailed content beneath them:

- Data Description.
- Model Description: model selection, model architecture, model hyperparameters.
- Evaluation Methods: choosing an appropriate evaluation metric.
- Report.

These headings are retained as planning topics. No missing architecture, hyperparameters or numerical results have been filled in.

## Software and resources

The source lists:

- Google Colab and Google Drive.
- Uploading data to Drive.
- Access to Hugging Face models.

## Roadmap

| Stage | Main task | Deliverable |
| --- | --- | --- |
| 1. Dataset audit | Download, visualize, count classes, check duplicates/leakage | EDA notebook |
| 2. Training pipeline | Dataset/Dataloader + pretrained ResNet | Working baseline |
| 3. Experiment tracking | Add W&B | Reproducible training runs |
| 4. Fine-tuning | Frozen vs unfrozen backbone | Transfer-learning comparison |
| 5. Model comparison | ResNet vs EfficientNet vs ConvNeXt | Main results table |
| 6. Analysis | Confusion matrix, errors, Grad-CAM | Figures + interpretation |
| 7. Packaging | GitHub README + clean code + report | Final portfolio |

## Schedule recorded in the source

The following entries are transcribed as written; they are not a revised schedule or a statement that milestones were achieved:

- Stages 1, 2: “Aug 19 - 28 Mordad”.
- Stages 3, 4: “Aug 26 - 4 Shahrivar”.
- Stages 5, 6, 7: “Sep 2 - 11 Shahrivar”.
- Stage 7: “Sep 9 - 15 Shahrivar”.

## Relationship to the portfolio

The later academic CV describes fine-tuning YOLOv8s for two-class object detection, three training experiments on an NVIDIA T4 GPU, ONNX export, and investigation of overlap across dataset splits. This source plan instead proposes image classification with ResNet, EfficientNet and ConvNeXt. The plan is preserved here as historical project documentation; it does not establish that those classification comparisons were carried out.

See the [portfolio project overview](../bird-vs-drone.html) for the later CV-based description.

## Transcription notes

- Headings, project description, resource list, roadmap and schedule were transcribed into readable Markdown.
- The roadmap's table structure was reconstructed from the Google Doc's text.
- Unrelated personal notes and private workspace/conversation links were omitted.
- The Google Doc was not modified.
- This is not a complete final thesis, a results report, a source-code release or an independently verified experiment record.
