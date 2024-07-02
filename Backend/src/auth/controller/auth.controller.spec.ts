import { Test, TestingModule } from "@nestjs/testing";
import { AuthController } from "./auth.controller";
import { SupabaseService } from "../../supabase/services/supabase.service";
import { AuthService } from "../services/auth.service";
import { supabase } from "../../supabase/lib/supabaseClient";
import { AuthDto } from '../dto/auth.dto';

describe("AuthController", () => {
    let controller: AuthController;
    let authService: AuthService;
    let supabaseService: SupabaseService;

    
    beforeEach(async () => {
        //mocking the supabase client
        const mockSupabase = {

        };
        const module: TestingModule = await Test.createTestingModule({
            controllers: [AuthController],
            providers: [
                AuthService,
                {
                    provide: SupabaseService,
                    useValue: {
                        signInWithSpotifyOAuth: jest.fn((x) => x),
                    },
                },
            ],
        }).compile();

        controller = module.get<AuthController>(AuthController);
        authService = module.get<AuthService>(AuthService);
        supabaseService = module.get<SupabaseService>(SupabaseService);
    });

    it("should be defined", () => {
        expect(controller).toBeDefined();
    });

    /*
    describe('getCurrentUser', () => {
        
        it('should return the current user', async () => {
            const response = await controller.getCurrentUser();
            expect(response).toStrictEqual({user: 'MockUser'});
        })

        it('should say "No user is signed in"', async () => {
            const response = await controller.getCurrentUser();
            expect(response).toThrow('No user is signed in');
        })
    })
        */
});
