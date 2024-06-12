import redis from 'redis';
import { promisify } from 'util';
import kue from 'kue';
import express from 'express';


// Create Redis client
const redisClient = redis.createClient();

// Promisify Redis functions
const setAsync = promisify(redisClient.set).bind(redisClient);
const getAsync = promisify(redisClient.get).bind(redisClient);

// Initialize number of available seats and reservation status
let numberOfAvailableSeats = 50;
let reservationEnabled = true;

// Function to reserve seats
const reserveSeat = async (number) => {
  await setAsync('available_seats', number.toString());
};

// Function to get current available seats
const getCurrentAvailableSeats = async () => {
  const seats = await getAsync('available_seats');
  return parseInt(seats) || 0;
};


// Create Kue queue
const queue = kue.createQueue();

// Initialize Express
const app = express();
const PORT = 1245;

// Middleware to parse JSON bodies
app.use(express.json());

// Route to get available seats
app.get('/available_seats', (req, res) => {
  res.json({ numberOfAvailableSeats: numberOfAvailableSeats });
});

// Route to reserve a seat
app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  // Create and queue a job
  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });
});

// Route to process the queue and reserve seats
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  // Process the queue
  queue.process('reserve_seat', async (job, done) => {
    try {
      const currentSeats = await getCurrentAvailableSeats();

      if (currentSeats === 0) {
        reservationEnabled = false;
        done(new Error('Not enough seats available'));
      } else {
        numberOfAvailableSeats--;
        await reserveSeat(numberOfAvailableSeats);
        if (numberOfAvailableSeats === 0) {
          reservationEnabled = false;
        }
        console.log(`Seat reservation job ${job.id} completed`);
        done();
      }
    } catch (error) {
      console.log(`Seat reservation job ${job.id} failed: ${error.message}`);
      done(error);
    }
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});