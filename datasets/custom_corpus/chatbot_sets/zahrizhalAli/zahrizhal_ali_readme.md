---
source: https://huggingface.co/datasets/ZahrizhalAli/mental_health_conversational_dataset/blob/main/README.md


dataset_info:
  features:
  - name: text
    dtype: string
  splits:
  - name: train
    num_examples: 175
license: mit
task_categories:
- text-generation
- conversational
language:
- en
tags:
- medical
pretty_name: Mental Health Chatbot Dataset
size_categories:
- n<1K
---
# CREDIT: Dataset Card for "heliosbrahma/mental_health_chatbot_dataset"

## Table of Contents

- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-instances)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)

## Dataset Description

### Dataset Summary

This dataset contains conversational pair of questions and answers in a single text related to Mental Health. Dataset was curated from popular healthcare blogs like WebMD, Mayo Clinic and HealthLine, online FAQs etc. All questions and answers have been anonymized to remove any PII data and pre-processed to remove any unwanted characters.

### Languages

The text in the dataset is in English.

## Dataset Structure

### Data Instances

A data instance include a text columns which is a conversational pair of questions and answers. Questions were asked by the patients and answers were given by healthcare providers.

### Data Fields

- 'text': conversational pair of questions and answers between patient and healthcare provider.

## Dataset Creation

### Curation Rationale

Chatbots offer a readily available and accessible platform for individuals seeking support. They can be accessed anytime and anywhere, providing immediate assistance to those in need. Chatbots can offer empathetic and non-judgmental responses, providing emotional support to users. While they cannot replace human interaction entirely, they can be a helpful supplement, especially in moments of distress.
Hence, this dataset was curated to help finetune a conversational AI bot using this custom dataset which can then be deployed and be provided to the end patient as a chatbot.

### Source Data

This dataset was curated from popular healthcare blogs like WebMD, Mayo Clinic and HealthLine, online FAQs etc.

### Personal and Sensitive Information

The dataset may contain sensitive information related to mental health. All questions and answers have been anonymized to remove any PII data.
