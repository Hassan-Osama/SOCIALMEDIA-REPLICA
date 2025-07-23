import { Request, Response } from 'express';
import prisma from '../prisma';

export const getCurrentUser = async (req: Request, res: Response) => {
  if (!req.userId) return res.status(401).json({ message: 'Unauthorized' });

  const user = await prisma.user.findUnique({
    where: { id: req.userId },
    select: { id: true, username: true, email: true, bio: true, avatarUrl: true }
  });

  if (!user) return res.status(404).json({ message: 'User not found' });

  res.json({ user });
};
