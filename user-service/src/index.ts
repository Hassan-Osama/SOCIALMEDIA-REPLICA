import express from 'express';
import dotenv from 'dotenv';
import authRoutes from './routes/authRoutes';
import userRoutes from './routes/userRoutes';

dotenv.config();

const app = express();
app.use(express.json());

app.use('/auth', authRoutes)
app.use('/api/user', userRoutes)

app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});
