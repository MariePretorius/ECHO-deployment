import { Test, TestingModule } from '@nestjs/testing';
import { YoutubeController } from './youtube.controller';
import { YoutubeService, YouTubeTrackInfo } from '../services/youtube.service';

describe('YoutubeController', () => {
  let controller: YoutubeController;
  let youtubeService: YoutubeService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [YoutubeController],
      providers: [
        {
          provide: YoutubeService,
          useValue: {
            getQueue: jest.fn(),
            fetchSingleTrackDetails: jest.fn(),
          },
        },
      ],
    }).compile();

    controller = module.get<YoutubeController>(YoutubeController);
    youtubeService = module.get<YoutubeService>(YoutubeService);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });

  describe('getQueue', () => {
    it('should return the result of youtubeService.getQueue', async () => {
        const mockResult: YouTubeTrackInfo[] = [{
            id: 'someId',
            title: 'Some Title',
            thumbnailUrl: 'http://example.com/thumbnail.jpg',
            channelTitle: 'Some Channel',
            videoUrl: 'http://example.com/video'
        }];
      const body = { artist: 'Artist Name', song_name: 'Song Name' };
      jest.spyOn(youtubeService, 'getQueue').mockResolvedValue(mockResult);

      const result = await controller.getQueue(body);

      expect(result).toBe(mockResult);
      expect(youtubeService.getQueue).toHaveBeenCalledWith(body.artist, body.song_name);
    });
  });

  describe('getTrackDetails', () => {
    it('should return the result of youtubeService.fetchSingleTrackDetails', async () => {
      const mockResult: YouTubeTrackInfo = {
        id: 'someId',
        title: 'Some Title',
        thumbnailUrl: 'http://example.com/thumbnail.jpg',
        channelTitle: 'Some Channel',
        videoUrl: 'http://example.com/video'
      };
      const body = { videoId: '123456' };
      jest.spyOn(youtubeService, 'fetchSingleTrackDetails').mockResolvedValue(mockResult);

      const result = await controller.getTrackDetails(body);

      expect(result).toBe(mockResult);
      expect(youtubeService.fetchSingleTrackDetails).toHaveBeenCalledWith(body.videoId);
    });
  });
});
