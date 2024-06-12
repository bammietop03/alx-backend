import { print, createClient } from 'redis';

const client = createClient();

client.on('connect', () => {
    console.log('Redis client connected to the server');
})

client.on('error', (err) => {
    console.log(`Redis client not connected to the server: ${err.message}`);
});

// Subscribe to the channel
client.subscribe('holberton school channel');

// Handle incoming messages
client.on('message', (channel, message) => {
  if (channel === 'holberton school channel') {
    console.log(message);
    if (message === 'KILL_SERVER') {
      client.unsubscribe('holberton school channel');
      client.quit();
    }
  }
});