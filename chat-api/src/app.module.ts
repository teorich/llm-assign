import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Conversation } from './conversation.entity';
import { ConversationService } from './conversation.service';
import { ConversationController } from './conversation.controller';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'sqlite',
      database: 'conversations.db',
      entities: [Conversation],
      synchronize: true,
    }),
    TypeOrmModule.forFeature([Conversation]),
  ],
  providers: [ConversationService],
  controllers: [ConversationController],
})
export class AppModule {}
