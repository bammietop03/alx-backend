const express = require('express');
import redis from 'redis';
import { promisify } from 'util';

const listProducts = [
    {
        id: '1',
        name: 'Suitcase 250',
        price: '50',
        stock: '4',
    },
    {
        id: '2',
        name: 'Suitcase 450',
        price: '100',
        stock: '10',
    },
    {
        id: '3',
        name: 'Suitcase 650',
        price: '350',
        stock: '2',
    },
    {
        id: '4',
        name: 'Suitcase 1050',
        price: '550',
        stock: '5',
    }
];

function getItemById(id) {
    let list = [];
    listProducts.forEach((product) => {
        if (product.id === id ) {
            list.push(product);
        };
    });

    return list;
};

// setting up express
const app = express();
const port = 1245;

app.use(express.json());

app.get('/list_products', (request, response) => {
    response.json(listProducts)
});




// Setting up redis
const client = redis.createClient();

// Promisify Redis functions to use async/await
const setAsync = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

// Function to reserve stock by itemId
const reserveStockById = (itemId, stock) => {
  const key = `item.${itemId}`;
  return setAsync(key, stock)
    .then(() => {
      console.log(`Reserved stock ${stock} for item ${itemId} in Redis`);
    })
    .catch((err) => {
      console.error(`Error reserving stock for item ${itemId}: ${err}`);
    });
};

// Async function to get current reserved stock by itemId
const getCurrentReservedStockById = async (itemId) => {
  const key = `item.${itemId}`;
  try {
    const reservedStock = await getAsync(key);
    return reservedStock;
  } catch (err) {
    console.error(`Error getting reserved stock for item ${itemId}: ${err}`);
    return null;
  }
};


// Route to get product by itemId
app.get('/list_products/:itemId', async (req, res) => {
    const itemId = req.params.itemId;
    
    // Find product by itemId
    const product = listProducts.find(p => p.id === itemId);
    if (!product) {
      return res.status(404).json({ error: 'Product not found' });
    }
  
    try {
      // Get current reserved stock from Redis
      const reservedStock = await getCurrentReservedStockById(itemId);
  
      // Add reserved stock to product info
      const productInfo = {
        id: product.id,
        name: product.name,
        price: product.price,
        reservedStock: reservedStock || 0 // Default to 0 if reservedStock is null
      };
  
      // Return product info with reserved stock
      res.json(productInfo);
    } catch (error) {
      console.error('Error:', error);
      res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Route to reserve product by itemId
app.get('/reserve_product/:itemId', async (req, res) => {
    const itemId = req.params.itemId;
    
    // Find product by itemId
    const product = listProducts.find(p => p.id === itemId);
    if (!product) {
      return res.status(404).json({ status: 'Product not found' });
    }
  
    try {
      // Check if there is enough stock available
      const reservedStock = await getCurrentReservedStockById(itemId);
      const availableStock = product.stock - (reservedStock || 0);
  
      if (availableStock <= 0) {
        return res.json({ status: 'Not enough stock available', itemId: itemId });
      }
  
      // Reserve one item
      await reserveStockById(itemId, reservedStock ? reservedStock + 1 : 1);
  
      // Return reservation confirmation
      res.json({ status: 'Reservation confirmed', itemId: itemId });
    } catch (error) {
      console.error('Error:', error);
      res.status(500).json({ error: 'Internal Server Error' });
    }
});
  

app.listen(port, () => {
    console.log(`Server is listening on port ${port}`);
});
