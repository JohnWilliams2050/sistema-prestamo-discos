import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DiscList } from './disc-list';

describe('DiscList', () => {
  let component: DiscList;
  let fixture: ComponentFixture<DiscList>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DiscList],
    }).compileComponents();

    fixture = TestBed.createComponent(DiscList);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
