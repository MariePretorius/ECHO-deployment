import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchComponent } from './search.component';
import { SearchService, Track } from '../../services/search.service';
import { of } from 'rxjs';
import { provideHttpClient, withInterceptorsFromDi } from "@angular/common/http";

describe('SearchComponent', () => {
  let component: SearchComponent;
  let fixture: ComponentFixture<SearchComponent>;
  let searchServiceMock: any;

  beforeEach(async () => {
    searchServiceMock = {
      getSearch: jest.fn().mockReturnValue(of([])),
      getAlbumSearch: jest.fn().mockReturnValue(of([])),
      getTopResult: jest.fn().mockReturnValue(of({} as Track)),
    };
    await TestBed.configureTestingModule({
      providers: [
        provideHttpClient(withInterceptorsFromDi()),
        SearchComponent,
        { provide: SearchService, useValue: searchServiceMock }
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SearchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call searchService methods and set observables', () => {
    expect(searchServiceMock.getSearch).toHaveBeenCalled();
    expect(searchServiceMock.getAlbumSearch).toHaveBeenCalled();
    expect(searchServiceMock.getTopResult).toHaveBeenCalled();
    expect(component.songs$).toBeTruthy();
    expect(component.albums$).toBeTruthy();
    expect(component.topResult$).toBeTruthy();
  });
});
