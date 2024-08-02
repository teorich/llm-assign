import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn } from 'typeorm';

@Entity()
export class Conversation {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  userId: string;

  @Column()
  model: string;

  @Column('text')
  prompt: string;

  @Column('text')
  response: string;

  @CreateDateColumn()
  createdAt: Date;
}
