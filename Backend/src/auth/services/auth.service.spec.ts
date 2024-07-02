// auth.service.spec.ts

import { Test, TestingModule } from "@nestjs/testing";
import { AuthService } from "./auth.service";
import { supabase } from '../../supabase/lib/supabaseClient';


jest.mock('../../supabase/lib/supabaseClient', () => ({
    supabase: {
        auth: {
            getUser: jest.fn(),
            signInWithPassword: jest.fn(),
        },
    },
}));

describe("AuthService", () => {
    let service: AuthService;

    beforeEach(async () => {
        const module: TestingModule = await Test.createTestingModule({
            providers: [AuthService],
          }).compile();
      
          service = module.get<AuthService>(AuthService);

    });

    it("should be defined", () => {
        expect(service).toBeDefined();
    });

    describe('getCurrentUser', () => {
        it('should return user if user is signed in', async () => {
            (supabase.auth.getUser as jest.Mock).mockResolvedValue({
              data: { user: { id: 'user-id', email: 'user@example.com' } },
            });
        
            const result = await service.getCurrentUser();
            expect(result).toEqual({ user: { id: 'user-id', email: 'user@example.com' } });
          });
        
          it('should throw an error if no user is signed in', async () => {
            (supabase.auth.getUser as jest.Mock).mockResolvedValue({
              data: { user: null },
            });
        
            await expect(service.getCurrentUser()).rejects.toThrow('No user is signed in');
          });
    });
    //EVERYTHING ABOVE HERE WORKS. DO NOT FUGGIN CHANGE IT

    describe('signIn', () => {
        it('should sign in successfully', async () => {
            const mockData = { user: { id: '123' }, session: { access_token: 'token' } };
            const mockResponse = { data: mockData, error: null };

            (supabase.auth.signInWithPassword as jest.Mock).mockResolvedValue(mockResponse);

            const authDto = { email: 'test@example.com', password: 'password' };
            const result = await service.signIn(authDto);

            expect(supabase.auth.signInWithPassword).toHaveBeenCalledWith({ email: 'test@example.com', password: 'password' });
            expect(result).toEqual(mockData);
        });

        it('should throw an error when sign in fails', async () => {
            const mockError = { message: 'Invalid credentials' };
            const mockResponse = { data: null, error: mockError };
        
            (supabase.auth.signInWithPassword as jest.Mock).mockResolvedValue(mockResponse);
        
            const authDto = { email: 'wrong@example.com', password: 'wrongpassword' };
        
            await expect(service.signIn(authDto)).rejects.toThrow('Invalid credentials');
            expect(supabase.auth.signInWithPassword).toHaveBeenCalledWith({ email: 'wrong@example.com', password: 'wrongpassword' });
          });
    });

});
