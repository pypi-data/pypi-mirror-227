import tensorflow as tf
import numpy as np


def positional_encoding(length, depth):
    """
    Generate positional encodings for sequences.

    Args:
        length (int): Length of the sequence.
        depth (int): Depth of the positional encoding.

    Returns:
        tf.Tensor: The positional encoding matrix.
    """
    depth = depth / 2

    positions = np.arange(length)[:, np.newaxis]  # (seq, 1)
    depths = np.arange(depth)[np.newaxis, :] / depth  # (1, depth)

    angle_rates = 1 / (10000 ** depths)  # (1, depth)
    angle_rads = positions * angle_rates  # (pos, depth)

    pos_encoding = np.concatenate(
        [np.sin(angle_rads), np.cos(angle_rads)],
        axis=-1)

    return tf.cast(pos_encoding, dtype=tf.float32)


class PositionalEmbedding(tf.keras.layers.Layer):
    """
    Positional embedding layer for transformer models.

    Args:
        vocab_size (int): Vocabulary size.
        dmodel (int): Model dimensionality. Aka embedding dims.
    """
    def __init__(self, vocab_size, dmodel):
        super().__init__()
        self.embedding = tf.keras.layers.Embedding(vocab_size, dmodel, mask_zero=True)
        self.pos_encoding = positional_encoding(2048, dmodel)
        self.dmodel = dmodel

    def call(self, input):
        x = self.embedding(input)
        x = x * tf.math.sqrt(tf.cast(self.dmodel, tf.float32))
        x = x + self.pos_encoding[tf.newaxis, :tf.shape(input)[1], :]
        return x


class _BaseAttention(tf.keras.layers.Layer):
    """
    Base attention layer for transformer models.

    Args:
        causal (bool): Whether the attention is causal or not.
        **kwargs: Additional arguments for MultiHeadAttention.
    """
    def __init__(self, causal, **kwargs):
        super().__init__()
        self.mha = tf.keras.layers.MultiHeadAttention(**kwargs)
        self.add = tf.keras.layers.Add()
        self.norm = tf.keras.layers.LayerNormalization()
        self.causal = causal


class SelfAttention(_BaseAttention):
    def call(self, input):
        x = self.mha(query=input, key=input, value=input, use_causal_mask=self.causal)
        x = self.add([x, input])
        x = self.norm(x)
        return x


class CrossAttention(_BaseAttention):
    def call(self, context, input):
        x = self.mha(query=input, key=context, value=context)
        x = self.add([input, x])
        x = self.norm(x)
        return x


class FeedForward(tf.keras.layers.Layer):
    """
    Feedforward neural network layer.

    Args:
        dff (int): Number of hidden units in the feedforward layer.
        dmodel (int): Model dimensionality.
        dropout_rate (float, optional): Dropout rate. Defaults to 0.1.
    """
    def __init__(self, dff, dmodel, dropout_rate=0.1):
        super().__init__()
        self.ff = tf.keras.Sequential([
            tf.keras.layers.Dense(dff, activation='relu'),
            tf.keras.layers.Dense(dmodel),
            tf.keras.layers.Dropout(dropout_rate)
        ])
        self.add = tf.keras.layers.Add()
        self.norm = tf.keras.layers.LayerNormalization()

    def call(self, input):
        x = self.ff(input)
        x = self.add([x, input])
        x = self.norm(x)
        return x


class EncoderLayer(tf.keras.layers.Layer):
    """
    Encoder layer of the transformer model.

    Args:
        dmodel (int): Model dimensionality.
        nheads (int): Number of attention heads.
        dff (int): Number of hidden units in the feedforward layer.
        dropout_rate (float, optional): Dropout rate. Defaults to 0.1.
    """
    def __init__(self, dmodel, nheads, dff, dropout_rate=0.1):
        super().__init__()
        self.attn = SelfAttention(causal=False, num_heads=nheads, key_dim=dmodel)
        self.ff = FeedForward(dff, dmodel=dmodel, dropout_rate=dropout_rate)

    def call(self, input):
        x = self.attn(input)
        x = self.ff(x)
        return x


class Encoder(tf.keras.layers.Layer):
    """
    Encoder module of the transformer model.

    Args:
        vocab_size (int): Vocabulary size.
        Nx (int): Number of encoder layers.
        dmodel (int): Model dimensionality.
        nheads (int): Number of attention heads.
        dff (int): Number of hidden units in the feedforward layer.
        dropout_rate (float, optional): Dropout rate. Defaults to 0.1.
    """
    def __init__(self, vocab_size, Nx, dmodel, nheads, dff, dropout_rate=0.1):
        super().__init__()
        self.dropout = tf.keras.layers.Dropout(dropout_rate)
        self.pos_embedding = PositionalEmbedding(vocab_size, dmodel)
        self.encoders = tf.keras.Sequential([
            EncoderLayer(dmodel, nheads, dff, dropout_rate=dropout_rate) for _ in range(Nx)
        ])

    def call(self, input):
        x = self.pos_embedding(input)
        x = self.dropout(x)
        x = self.encoders(x)
        return x


class DecoderLayer(tf.keras.layers.Layer):
    """
    Decoder layer of the transformer model.

    Args:
        dmodel (int): Model dimensionality.
        nheads (int): Number of attention heads.
        dff (int): Number of hidden units in the feedforward layer.
        dropout_rate (float, optional): Dropout rate. Defaults to 0.1.
    """
    def __init__(self, dmodel, nheads, dff, dropout_rate=0.1):
        super(DecoderLayer, self).__init__()
        self.mha = SelfAttention(True, num_heads=nheads, key_dim=dmodel)
        self.cmha = CrossAttention(False, num_heads=nheads, key_dim=dmodel)
        self.ff = FeedForward(dff, dmodel, dropout_rate=dropout_rate)

    def call(self, input, context):
        x = self.mha(input)
        x = self.cmha(input=input, context=context)
        x = self.ff(x)
        return x


class Decoder(tf.keras.layers.Layer):
    """
    Decoder module of the transformer model.

    Args:
        vocab_size (int): Vocabulary size.
        Nx (int): Number of decoder layers.
        dmodel (int): Model dimensionality.
        nheads (int): Number of attention heads.
        dff (int): Number of hidden units in the feedforward layer.
        dropout_rate (float, optional): Dropout rate. Defaults to 0.1.
    """
    def __init__(self, vocab_size, Nx, dmodel, nheads, dff, dropout_rate=0.1):
        super(Decoder, self).__init__()
        self.pos_encoding = PositionalEmbedding(vocab_size, dmodel)
        self.dropout = tf.keras.layers.Dropout(dropout_rate)
        self.decoders = [DecoderLayer(dmodel, nheads, dff, dropout_rate) for _ in range(Nx)]

    def call(self, input, context):
        x = self.pos_encoding(input)
        x = self.dropout(x)
        for dec in self.decoders:
            x = dec(x, context)
        return x


class Transformer(tf.keras.layers.Layer):
    """
    Transformer model.

    Args:
        vocab_size (int): Vocabulary size.
        output_dims (int): Dimensionality of the output.
        Nx (int): Number of encoder and decoder layers.
        dmodel (int): Model dimensionality.
        nheads (int): Number of attention heads.
        dff (int): Number of hidden units in the feedforward layer.
        dropout_rate (float, optional): Dropout rate. Defaults to 0.1.
    """
    def __init__(self, vocab_size, output_dims, Nx, dmodel, nheads, dff, dropout_rate=0.1):
        super().__init__()
        self.encoder = Encoder(vocab_size=vocab_size, Nx=Nx, dmodel=dmodel, nheads=nheads, dff=dff,
                               dropout_rate=dropout_rate)
        self.decoder = Decoder(vocab_size=vocab_size, Nx=Nx, dmodel=dmodel, nheads=nheads, dff=dff,
                               dropout_rate=dropout_rate)
        self.logits_output = tf.keras.layers.Dense(output_dims)
        self.softmax = tf.keras.activations.softmax

    def call(self, inputs):
        context, prognosticatee = inputs

        context = self.encoder(context)
        x = self.decoder(prognosticatee, context)

        x = self.logits_output(x)
        if hasattr(x, "_keras_mask"):
            del x._keras_mask
        x = self.softmax(x)

        return x
