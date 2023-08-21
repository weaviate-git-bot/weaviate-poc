{
  "classes": [
    {
      "class": "Document",
      "description": "A class called document",
      ...,
      "moduleConfig": {
        "generative-openai": {
          "model": "gpt-3.5-turbo",  // Optional - Defaults to `gpt-3.5-turbo`
          "resourceName": "<YOUR-RESOURCE-NAME>",  // For Azure OpenAI - Required
          "deploymentId": "<YOUR-MODEL-NAME>",  // For Azure OpenAI - Required
          "temperatureProperty": <temperature>,  // Optional, applicable to both OpenAI and Azure OpenAI
          "maxTokensProperty": <max_tokens>,  // Optional, applicable to both OpenAI and Azure OpenAI
          "frequencyPenaltyProperty": <frequency_penalty>,  // Optional, applicable to both OpenAI and Azure OpenAI
          "presencePenaltyProperty": <presence_penalty>,  // Optional, applicable to both OpenAI and Azure OpenAI
          "topPProperty": <top_p>,  // Optional, applicable to both OpenAI and Azure OpenAI
        },
      }
    }
  ]
}