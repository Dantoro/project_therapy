[GitHub - thu-coai/Emotional-Support-Conversation: Data and codes for ACL 2021 paper: Towards Emotional Support Dialog Systems](https://github.com/thu-coai/Emotional-Support-Conversation)


[README.md · thu-coai/esconv at main](https://huggingface.co/datasets/thu-coai/esconv/blob/main/README.md)


original esconv.json: 910 rows

valid and test: 195 each

train: the same 910 rows as the original

esconv_2: hard to tell, looks a lot bigger. 

either combine train+test+valid, or use esconv2, and figure out which of these models im actually using between github and huggingface. 

huggingface has emotion_types, but github has strategy_types. i might want to get a values_count on one of those, and possibly cross-reference it with the ekman categories, and pick a subset of samples to use.


each row has a single dialog column with an entire conversation in it. once we isolate which rows we want, we're gonna have to manually split each cell into its constitution dialog pairs by using the speaker-user and speaker-sys tags. 

its gonna be a pain in the neck, and might not be worthwhile. but it could get us a lot more data samples.
