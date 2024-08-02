import { Controller, Get, Post, Body, Param } from '@nestjs/common';
import { ConversationService } from './conversation.service';
import axios from 'axios';

@Controller('conversations')
export class ConversationController {
  constructor(private readonly conversationService: ConversationService) {}

  @Post()
  async create(@Body() createConversationDto: any) {
    const { model, prompt, userId } = createConversationDto;
    const response = await this.sendQueryToFlask(model, prompt);
    return this.conversationService.create(userId, model, prompt, response);
  }

  @Get()
  async findAll() {
    return this.conversationService.findAll();
  }

  @Get(':id')
  async findOne(@Param('id') id: string) {
    return this.conversationService.findOne(+id);
  }

  @Get('user/:userId')
  async findByUser(@Param('userId') userId: string) {
    return this.conversationService.findByUser(userId);
  }

  private async sendQueryToFlask(model: string, prompt: string): Promise<string> {
    const response = await axios.post('http://flask-chat-app:5000/chat', {
      model,
      prompt,
      user_id: 'default_user',
    });
    return response.data.response;
  }
}
