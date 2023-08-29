from tensorflow import matmul, math, cast, float32
from tensorflow.keras.layers import Layer
from tensorflow.keras.backend import softmax

class DotProductAttention(Layer):
    """ class for scaled dot product attention """

    def __init__(self, **kwargs):
        super(DotProductAttention, self).__init__(**kwargs)

    def call(self, queries, keys, values, d_k, mask=None):
        """ method for scaled dot product attention

        Parameters
        ----------
        queries :
            query vector
            
        keys :
            key vector
            
        values :
            values vector
            
        d_k : int
            dimensionality of the linearly projected queries and keys
            
        mask :
             (Default value = None)

        Returns
        -------
        outputs :
            scaled dot product attention outputs            

        """

        scores = matmul(queries, keys, transpose_b=True) / math.sqrt(cast(d_k, float32))

        if mask is not None:
            scores += -1e9 * mask
        
        weights = softmax(scores)

        return matmul(weights, values)