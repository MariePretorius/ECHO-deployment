import { BottomNavComponent } from './bottom-nav.component';
import { MoodService } from "./../../services/mood-service.service";
import { Router } from '@angular/router';

describe('BottomNavComponent', () => {
  let component: BottomNavComponent;
  let moodService: MoodService;
  let router: Router;

  beforeEach(() => {
    // Mock the Router
    router = {
      navigate: jest.fn()
    } as any;

    // Mock the MoodService
    moodService = {
      getComponentMoodClasses: jest.fn().mockReturnValue([]),
      getBackgroundMoodClasses: jest.fn().mockReturnValue([]),
      getComponentMoodClassesDark: jest.fn().mockReturnValue([])
    } as any;

    // Initialize the component with the mocked router and moodService
    component = new BottomNavComponent(router, moodService);
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should navigate to /home when goHome is called', () => {
    component.goHome();
    expect(router.navigate).toHaveBeenCalledWith(['/home']);
  });

  it('should navigate to /search when goSearch is called', () => {
    component.goSearch();
    expect(router.navigate).toHaveBeenCalledWith(['/search']);
  });

  it('should navigate to /insights when goInsights is called', () => {
    component.goInsights();
    expect(router.navigate).toHaveBeenCalledWith(['/insights']);
  });

  it('should navigate to /library when goLibrary is called', () => {
    component.goLibrary();
    expect(router.navigate).toHaveBeenCalledWith(['/library']);
  });
});