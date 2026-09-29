import { TestBed } from '@angular/core/testing';
import { Disc } from './disc';

describe('Disc', () => {
  let service: Disc;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Disc);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
