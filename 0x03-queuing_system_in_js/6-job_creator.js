const kue = require('kue');
const queue = kue.createQueue();

const job = queue.create('push_notification_code', {
    phoneNumber: '1234567890',
    message: 'This is a test',
}).save((err) => {
    if (!err) {
        console.log(`Notification job created: ${job.id}`);
    } else {
        console.error('Error creating job:', err);
    }
});

// Event handlers for the job
job.on('complete', () => {
    console.log('Notification job completed');
}).on('failed', () => {
    console.log('Notification job failed');
});