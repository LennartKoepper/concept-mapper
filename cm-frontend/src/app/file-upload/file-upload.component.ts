import { CommonModule} from '@angular/common';
import { Component, ViewChild, ElementRef  } from '@angular/core';
import { ApiService } from '../_services/api.service';
import { throwError } from 'rxjs';
import { OptionsComponent } from '../options/options.component';

@Component({
  selector: 'app-file-upload',
  standalone: true,
  imports: [CommonModule, OptionsComponent],
  templateUrl: './file-upload.component.html',
  styleUrl: './file-upload.component.scss'
})
export class FileUploadComponent {

  status: "initial" | "waiting" | "processing" | "success" | "fail" = "initial"; 
  file: File | null = null;

  constructor(private api: ApiService) {}

  @ViewChild(OptionsComponent) optionsForm!:OptionsComponent;
  @ViewChild('fileInput') fileInputVariable!: ElementRef;

  onChange(event: Event) {
    if (!event.currentTarget) {
      this.file = null;
    } else {
      this.file = ((event.target as HTMLInputElement).files as FileList)[0];
    }

    if (this.file) {
      this.status = "waiting";
    }
  }

  onUpload() {
    if (this.file) {
      const formData = new FormData();
      formData.append('file', this.file, this.file.name);
  
      let options = this.optionsForm.getOptions()

      this.status = 'processing';
      
      this.api.postFile(formData, options).subscribe({
        next: res => this.status = 'success',
        error: err => this.status = 'fail'
      });
    }
  }

  onClear() {
    if (this.status == 'processing') {
      return;
    }
    
    this.status = 'initial'
    this.file = null;
    this.fileInputVariable.nativeElement.value = "";
    this.optionsForm.resetOptions();
  }
}
