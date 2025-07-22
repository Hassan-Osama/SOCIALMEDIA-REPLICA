import { Request, Response } from 'express';
import prisma from '../prisma';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { registerSchema, loginSchema } from '../utils/validators';

const JWT_SECRET = process.env.JWT_SECRET!;

export const register = async (req: Request, res: Response) => {
  const parse = registerSchema.safeParse(req.body);
  if (!parse.success) return res.status(400).json({ errors: parse.error.format() });

  const { username, email, password } = parse.data;

  const existing = await prisma.user.findFirst({ where: { OR: [{ username }, { email }] } });
  if (existing) return res.status(400).json({ message: 'Username or email already taken' });

  const hashed = await bcrypt.hash(password, 10);

  const user = await prisma.user.create({
    data: { username, email, password: hashed },
  });

  const token = jwt.sign({ userId: user.id }, JWT_SECRET, { expiresIn: '7d' });

  return res.status(201).json({ token, user: { id: user.id, username, email } });
};

export const login = async (req: Request, res: Response) => {
  const parse = loginSchema.safeParse(req.body);
  if (!parse.success) return res.status(400).json({ errors: parse.error.format() });

  const { email, password } = parse.data;

  const user = await prisma.user.findUnique({ where: { email } });
  if (!user) return res.status(401).json({ message: 'Invalid credentials' });

  const valid = await bcrypt.compare(password, user.password);
  if (!valid) return res.status(401).json({ message: 'Invalid credentials' });

  const token = jwt.sign({ userId: user.id }, JWT_SECRET, { expiresIn: '7d' });

  return res.json({ token, user: { id: user.id, username: user.username, email } });
};
