# Chatbot Logic

**Last updated: 2025-07-07**

---

## Overview

This is primarily a blackbox so far. I will use an autoregressor transformer as the main engine of this generative chatbot, although it will have a rules-based component and a retrieval-based component as well. These might be part of the decisionMaker rather than the Chatbot itself though.

Upon outputting a chatbotResponse, the chatbotResponse will be postprocessed through the shallow character-level CNN described in **cnn_model.md,** and then the rawText and cnnVector will both be appended to the Short-Term Memory alongside the rawText and cnnVector of their corresponding userInput.
