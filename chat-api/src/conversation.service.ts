import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Conversation } from './conversation.entity';

@Injectable()
export class ConversationService {
  constructor(
    @InjectRepository(Conversation)
    private readonly conversationRepository: Repository<Conversation>,
  ) {}

  async create(userId: string, model: string, prompt: string, response: string): Promise<Conversation> {
    const conversation = new Conversation();
    conversation.userId = userId;
    conversation.model = model;
    conversation.prompt = prompt;
    conversation.response = response;
    return this.conversationRepository.save(conversation);
  }

  async findAll(): Promise<Conversation[]> {
    return this.conversationRepository.find({ order: { createdAt: 'DESC' } });
  }

  async findOne(id: number): Promise<Conversation> {
    return this.conversationRepository.findOne({where: {id}});
  }

  async findByUser(userId: string): Promise<Conversation[]> {
    return this.conversationRepository.find({
      where: { userId },
      order: { createdAt: 'DESC' },
    });
  }
}
