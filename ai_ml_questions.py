"""Common AI and machine-learning interview prompts expanded into 100 study questions."""

from web_questions import build_library


AI_ML_TOPICS = [
    ('artificial intelligence', 'Artificial intelligence is the broad field of building systems that perform tasks associated with human intelligence, such as reasoning or perception.', 'Equating all AI with machine learning ignores rules, search, planning, and other AI approaches.'),
    ('machine learning', 'Machine learning learns patterns from data to make predictions or decisions rather than relying only on hand-written rules.', 'A model is not useful unless its training data, objective, and deployment context are appropriate.'),
    ('deep learning', 'Deep learning uses multi-layer neural networks to learn representations from large amounts of data.', 'Using deep learning for small tabular data without a baseline can add cost without improving results.'),
    ('neural networks', 'Neural networks compose weighted transformations and nonlinear activations to approximate complex functions.', 'More layers and parameters do not automatically improve generalization.'),
    ('activation functions', 'Activations introduce nonlinearity; common choices include ReLU, sigmoid, tanh, and GELU.', 'Using sigmoid repeatedly in deep hidden layers can contribute to vanishing gradients.'),
    ('backpropagation', 'Backpropagation applies the chain rule to compute gradients of loss with respect to model parameters.', 'Gradient calculations are only useful when the forward computation and loss are correctly defined.'),
    ('gradient descent', 'Gradient descent updates parameters in the direction that reduces loss using computed gradients.', 'A poor learning rate can make training unstable or extremely slow.'),
    ('stochastic gradient descent', 'SGD estimates gradients from a mini-batch, trading noisy updates for scalable training.', 'Batch size changes optimization behavior and should not be chosen without validation.'),
    ('learning rate schedules', 'Schedules change the learning rate during training, such as decay, warmup, or cosine schedules.', 'Changing schedules while comparing experiments can confound which change caused an improvement.'),
    ('loss functions', 'A loss function measures prediction error, such as cross-entropy for classification or MSE for regression.', 'Optimizing a convenient loss that does not reflect business cost can produce the wrong model behavior.'),
    ('regularization', 'Regularization discourages overly complex models through methods such as L1, L2, dropout, or early stopping.', 'Regularization strength must be selected using validation data, not guessed.'),
    ('dropout', 'Dropout randomly disables units during training to reduce co-adaptation and overfitting.', 'Dropout is normally disabled or scaled differently at inference time.'),
    ('batch normalization', 'Batch normalization normalizes intermediate activations to stabilize and often accelerate training.', 'Its behavior differs between training and inference, so mode handling matters.'),
    ('convolutional neural networks', 'CNNs use local filters and shared weights to learn spatial patterns in images and related data.', 'Discarding spatial resolution too aggressively can lose details needed for prediction.'),
    ('recurrent neural networks', 'RNNs process sequences by carrying hidden state across positions.', 'Basic RNNs struggle with long dependencies because gradients can vanish or explode.'),
    ('LSTM networks', 'LSTMs use gates and a cell state to preserve useful information across longer sequences.', 'They are not automatically better than transformers for every sequence task.'),
    ('transformers', 'Transformers use attention to model relationships among tokens in parallel.', 'Attention cost grows quickly with sequence length in standard implementations.'),
    ('self-attention', 'Self-attention computes weighted interactions between positions in the same sequence.', 'Attention weights are not a complete or reliable explanation of model reasoning.'),
    ('large language models', 'LLMs are large transformer models trained on text to predict tokens and perform language tasks.', 'Fluent output can still be incorrect, biased, or unsupported by evidence.'),
    ('prompt engineering', 'Prompt engineering structures instructions, examples, context, and output constraints to improve model behavior.', 'Prompts do not replace evaluation, retrieval quality, safety checks, or product design.'),
    ('retrieval-augmented generation', 'RAG retrieves relevant external documents and supplies them as context to a generative model.', 'Poor retrieval or untrusted documents can still lead to inaccurate answers.'),
    ('model evaluation', 'Evaluation measures quality with task metrics, representative test sets, error analysis, and human review when needed.', 'A single aggregate metric can conceal failures for important user groups or use cases.'),
    ('model drift', 'Drift occurs when data, relationships, or user behavior changes so production performance degrades.', 'Monitoring only uptime misses silent quality degradation.'),
    ('MLOps', 'MLOps applies engineering practices to reproducible data pipelines, training, deployment, monitoring, and governance.', 'Deploying a notebook model without versioning, monitoring, or rollback is not a reliable ML system.'),
    ('responsible AI', 'Responsible AI considers fairness, privacy, safety, transparency, and accountability throughout the lifecycle.', 'Treating responsible AI as a final checklist instead of a design requirement creates avoidable harm.'),
]

AI_ML_QUESTIONS = build_library(AI_ML_TOPICS)
