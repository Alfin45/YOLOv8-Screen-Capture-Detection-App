## TENTANG PROGRAM
![Bannergithub](https://github.com/Alfin45/YOLOv8-Screen-Capture-Detection-App/assets/161688299/19e54aff-58d1-4c1d-b7c3-cc98c38121a2)

<pre>
Program ini dibuat dengan tujuan mendeteksi apapun yang ada di dalam layar monitor 
pada bagian kiri dengan YOLOv8 dan sebagai bentuk project tugas akhir.
  Fitur : 
  1. Detect(Play/Pause)
  2. Sharpen
  3. Ganti HSL
  4. Save di dalam folder appneed/result/
  5. Disable Screen(Idle)
  6. Konfigurasi IoU, Conf, dan imgsz

  Note : Accuracy 4 level : level 1 (1-25) <- default:640
                            level 2 (26-50) <- 736
                            level 3 (51-75) <- 800
                            level 4 (76-100) <- 960
</pre>


## TRAINING MODEL
![Bannergithub2](https://github.com/Alfin45/YOLOv8-Screen-Capture-Detection-App/assets/161688299/55d60f0f-eb6a-475e-ab4a-57a28593dcde)

<pre>
  Pada repo ini masih menggunakan training model untuk mendeteksi no helmet, no gloves, dan no jacket
  Note:
  custom training model(appneed/last.pt) yang digunakan dalam mendeteksi masih kecil precision, recall, 
  mAP50 dan mAP50-95 dikarnakan ini hanya dataset contoh untuk membuat program berjalan.
  Display orientation harus kurang dari 1920 x 1080.(Rekomendasi 1600 x 900) 
</pre>



## PREVIEW PROGRAM
![previewProgram](https://github.com/Alfin45/YOLOv8-Screen-Capture-Detection-App/assets/161688299/f956cb1b-0abf-4d12-a619-8d551e9bda87)
![PreviewVid (online-video-cutter com) (1)](https://github.com/Alfin45/YOLOv8-Screen-Capture-Detection-App/assets/161688299/f174a89f-c908-4583-9daf-3e7f6a743b37)






