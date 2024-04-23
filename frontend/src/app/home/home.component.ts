import { Component, OnInit } from '@angular/core';
import { UploadService } from '../services/upload.service';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
  loading = false;
  load = true;
  selectedColunms: any[] = [];
  allColunms = ['PName', 'Customer Age']
  constructor(private uploadService: UploadService) { }
  ngOnInit(): void {
  }
  allData: any[] = []

  iterationCount: number[] = Array.from({ length: 5 }, (_, index) => index);
  columnNumber: number = 7
  imageUrl: any[] = [];

  // handleAddClick() {
  //   this.allowRemove = false
  //   this.iterationCount.push(this.iterationCount[this.iterationCount.length - 1] + 1);
  //   if (this.iterationCount.length > 7) {
  //     this.allowAdd = true;
  //   }
  // }
  // handleRemoveClick() {
  //   this.allowAdd = false;
  //   this.iterationCount = this.iterationCount.filter(x => x < this.iterationCount[this.iterationCount.length - 1]);
  //   if (this.iterationCount.length <= 2) {
  //     this.allowRemove = true;
  //   }
  // }
  scroll(el: HTMLElement) {
    el.scrollIntoView({ behavior: 'smooth' });
  }

  message: string | null = null;
  selectedFile: File | null = null;
  onFileChange(event: any) {
    this.selectedFile = event.target.files[0];
  }
  hideloader() {
    let d = document.getElementById('loading');
    if (d)
      d.style.display = 'none';
  }
  uploadFile() {
    if (!this.selectedFile) {
      this.message = 'Please select a file.';
      return;
    }
    this.load = false;
    this.loading = true;
    this.allData = []
    this.imageUrl = [];
    this.uploadService.uploadFile(this.selectedFile)
      .subscribe(
        (data) => {

          this.allData = data
          console.log(this.allData)
          for (let index = 0; index < data.length; index++) {
            this.imageUrl.push(btoa(String.fromCharCode.apply(null, data[index].image_data.data)));
          }
          this.load = true;
          this.loading = true
        }
      );
  }

}
