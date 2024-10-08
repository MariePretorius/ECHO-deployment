import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SvgIconComponent } from './svg-icon.component';
import { ThemeService } from './../../services/theme.service';
import { By } from '@angular/platform-browser';

describe('SvgIconComponent', () => {
  let component: SvgIconComponent;
  let fixture: ComponentFixture<SvgIconComponent>;
  let mockThemeService: Partial<ThemeService>;

  beforeEach(async () => {
    // Mock ThemeService or any other dependencies
    mockThemeService = {
      isDarkModeActive: jest.fn().mockReturnValue(true) // Example mock implementation
    };

    await TestBed.configureTestingModule({
      imports: [SvgIconComponent],
      providers: [
        { provide: ThemeService, useValue: mockThemeService }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(SvgIconComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should emit svgClick event when clicked', () => {
    jest.spyOn(component.svgClick, 'emit');
    const svgElement = fixture.debugElement.query(By.css('svg'));
    svgElement.triggerEventHandler('click', null);
    expect(component.svgClick.emit).toHaveBeenCalled();
  });
/*
  it('should correctly toggle circleColor based on theme', () => {
    expect(component.circleColor).toBe('rgb(238, 2, 88)');
    (mockThemeService.isDarkModeActive as jest.Mock).mockReturnValue(false);
    fixture.detectChanges();
    expect(component.circleColor).toBe('rgba(238, 2, 88, 0.5)');
  });
  */
});