import pydicom as dicom
import os
import tempfile

#В первую очередь импортируем необходимые библиотеки, 
#пайдиком будет читать файлы, 
#ось будет перемещать и переименовывать

dd = 'D:/test_work_fv/src' # Переменная с путём до изображения, приставка FW в директории означает Final View
dcm_dir = os.listdir(dd) # переменная превращается в список с именами файлов в директории

#функция по удалению личных данных пациентов, dcm_input - этой файл на входе, z - рабочая переменная функции, в ней открывается файл для чтения
def anonymyze(dir_path):
    for dcm_input in dir_path:
        z = dicom.dcmread('D:/test_work_fv/src/{}'.format(dcm_input))
        data_elements = ['PatientID',
                'PatientBirthDate']
        output_filename = tempfile.NamedTemporaryFile().name
        z.save_as('D:/test_work_fv/src/{}'.format(dcm_input))
        try:
            z.PatientName = "Name"
            z.PatientID = "id"
            output_filename = tempfile.NamedTemporaryFile().name
            z.save_as('D:/test_work_fv/src/{}'.format(dcm_input))
        except AttributeError:
            z.PatientID = "id"
            output_filename = tempfile.NamedTemporaryFile().name
            z.save_as('D:/test_work_fv/src/{}'.format(dcm_input))
    print("Files anonymyzed and saved")   
#некоторые файлы в директории не имели атрибута имени и возвращали ошибку, поэтому делаем через try/except

#функция по созданию 10 папок первого ключа, цикл читает каждый файл и создаёт папку по значению StudyInstanceUID, если такая папка уже есть - просто пропускает
def create_1st_key(dir_path):
    for dcm_input in dir_path:
        z = dicom.dcmread('D:/test_work_fv/src/{}'.format(dcm_input))
        try: 
            os.mkdir("D:/test_work_fv/new_data_structure/{}".format(z.StudyInstanceUID))
        except FileExistsError:
            pass
    print("First level Folders created")    

#создаём папки по второму ключу, принцип точно такой же
def create_2nd_key(dir_path):  
    for dcm_input in dir_path:
        z = dicom.dcmread('D:/test_work_fv/src/{}'.format(dcm_input))
        try:
            os.mkdir("D:/test_work_fv/new_data_structure/{}/{}".format(z.StudyInstanceUID, z.SeriesInstanceUID))
        except FileExistsError:
            pass
    print("Second level Folders created")    

#распределяем файлы по SOPInstanceUID с помощью rename(), на входе у ренейма исходный файл, а сохранится он как новый и за имя возьмёт SOPInstanceUID
def rename_sort(dir_path):
    for dcm_input in dir_path:
        z = dicom.dcmread('D:/test_work_fv/src/{}'.format(dcm_input))
        with open("indexes.txt", "a") as indexes_file:
            indexes_file.write("File {} old place: {}".format(dcm_input, "D:/test_work_fv/src/" + dcm_input + " "))
        os.rename("D:/test_work_fv/src/{}".format(dcm_input), "D:/test_work_fv/new_data_structure/{}/{}/{}".format(z.StudyInstanceUID, z.SeriesInstanceUID, z.SOPInstanceUID + ".dcm "))
        with open("indexes.txt", "a") as indexes_file:
            indexes_file.write("File {} new place: {}".format(dcm_input, "D:/test_work_fv/new_data_structure/{}/{}/{}".format(z.StudyInstanceUID, z.SeriesInstanceUID, z.SOPInstanceUID + ".dcm\n")))
    print("Files renamed and sorted")
    print("New folders and names writen in indexes.txt in the same folder")

#функция мейн в которой мы вызываем все остальные функции
def main(dir_path):
    anonymyze(dir_path)
    create_1st_key(dir_path)
    create_2nd_key(dir_path)
    rename_sort(dir_path)
#начало функции
if __name__ == '__main__':
    main(dcm_dir)

