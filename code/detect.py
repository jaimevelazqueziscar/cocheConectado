# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo which runs object detection on camera frames using GStreamer.

Run default object detection:
python3 detect.py

Choose different camera and input encoding
python3 detect.py --videosrc /dev/video1 --videofmt jpeg

TEST_DATA=../all_models
Run face detection model:
python3 detect.py \
  --model ${TEST_DATA}/mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite

Run coco model:
python3 detect.py \
  --model ${TEST_DATA}/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite \
  --labels ${TEST_DATA}/coco_labels.txt
"""
import argparse
import collections
import common
import gstreamer
import numpy as np
import os
import re
import svgwrite
import time
import pygame
import sys
from pygame.locals import *
import io
import datetime
import connection
Object = collections.namedtuple('Object', ['id', 'score', 'bbox'])


nCoches = 0
tpo = 0
t1 = 0
n = 0

def load_labels(path):
    p = re.compile(r'\s*(\d+)(.+)')
    with open(path, 'r', encoding='utf-8') as f:
       lines = (p.match(line).groups() for line in f.readlines())
       return {int(num): text.strip() for num, text in lines}

def shadow_text(dwg, x, y, text, font_size=20):
    dwg.add(dwg.text(text, insert=(x+1, y+1), fill='black', font_size=font_size))
    dwg.add(dwg.text(text, insert=(x, y), fill='white', font_size=font_size))

def print_simulation(x0, y0, x1, y1, carsim, display, dist_max):
    width, height = 480, 640
    area = (x1-x0)*(y1-y0)
    green = (0, 255, 0)
    if area < 0.25:
        dist_m = 0.3/area #cáculo de la distancia en metros
        dist_esc = (0.4*width/dist_max)*dist_m #escalado para representación

        if (x1+x0)/2 > 1 - y1 and (x1+x0)/2 < y1: #en mi carril
            pygame.draw.polygon(carsim, green, [(height/2 - height/30, width/2 - width/30 - width/15 - dist_esc), (height/2 +  height/30, width/2 - width/30 - width/15 - dist_esc), (height/2 + height/30, width/2 + width/30 - width/15 - dist_esc), (height/2 - height/30, width/2 + width/30 - width/15 - dist_esc)])
        if (x1+x0)/2 > y1 and (x1+x0)/2 < ((y1 - 0.35)/0.3): #en el carril derecho
            pygame.draw.polygon(carsim, green, [(height/2 + height/5 - height/30, width/5 - width/30 - dist_esc), (height/2 + height/5 + height/30, width/5 - width/30 - dist_esc), (height/2 + height/5 + height/30, width/5 + width/30 - dist_esc), (height/2 + height/5 - height/30, width/5 + width/30 - dist_esc)])
        if (x1+x0)/2 > ((0.65-y1)/0.3) and (x1+x0)/2 < 1 - y1: #en el carril izquierdo
            pygame.draw.polygon(carsim, green, [(height/2 - height/5 - height/30, width/5 - width/30 - dist_esc), (height/2 - height/5 + height/30, width/5 - width/30 - dist_esc), (height/2 - height/5 + height/30, width/5 + width/30 - dist_esc), (height/2 - height/5 - height/30, width/5 + width/30 - dist_esc)])
        display.blit(carsim, (0, 0))
        pygame.display.flip()

def load_temp():

    data = np.loadtxt("/sys/devices/virtual/thermal/thermal_zone0/temp")
    return data



def semaforo_mode(x0, y0, x1, y1, maxVel):
    global nCoches
    global t1
    global n
    area = (x1-x0)*(y1-y0)
    if area > 0.15 and nCoches > 20:
        t1 = time.time()
        resultados = open("result_detect " + str(n) + ".txt", "w")
        n += 1
        #print ("Introducir la velocidad actual del vehículo: ")
        vel = np.loadtxt('velocidad.txt')
        if int(vel) == 0:
            print ("Entramos en modo semáforo")
            print ("Solicitamos prioridad para ejecutar")
            archivo = open("prioridad_bt.txt","w")
            archivo.write("semaforo")
            archivo.close()

            while True:
                datos = np.loadtxt('prioridad_bt.txt', dtype = "str")
                if datos == "OK":
                    print ("Prioridad concedida")
                    break
                time.sleep(0.1)
            print ("Tiempo hasta que la prioridad fue concedida = ", time.time() - t1)
            resultados.write("Tiempo hasta que la prioridad fue concedida = " + str(time.time() - t1) + "\n")
            t1 = time.time()

            print ("Buscando semáforos...")
            addrSemaforo = connection.solicitud_semaforo(maxVel, 3)
            print ("Tiempo hasta que se detectó un semáforo = ", time.time() - t1)
            resultados.write("Tiempo hasta que se detectó un semáforo = " + str(time.time() - t1) + "\n")
            t1 = time.time()
            velocidad, momento = connection.confirmacion_semaforo(3, addrSemaforo)
            if velocidad == 0:
                print ("Operación abortada. Cada uno fija su velocidad y su momento de salida")
                resultados.write("Tiempo hasta que se recibieron las directrices del semáforo = " + str(time.time() - t1) + "\n")
                t1 = time.time()
            else:
                print ("Salida a " + str(velocidad) + "km/h")
                print ("Salida en el momento fijado: ", momento)
                momento = momento.split(" ")
                print (momento)
                momento = momento[1].split(".")
                print (momento)
                momento = datetime.datetime.strptime(momento[0], '%H:%M:%S')
                print (momento)
                print ("Tiempo hasta que se recibieron las directrices del semáforo = ", time.time() - t1)
                resultados.write("Tiempo hasta que se recibieron las directrices del semáforo = " + str(time.time() - t1) + "\n")
                t1 = time.time()

                while True:
                    now = datetime.datetime.now()
                    if now.minute == momento.minute and now.second >= momento.second:
                        print (now)
                        print (momento)
                        print ("Semáforo en verde. Arrancar!")
                        break
                print ("Este tiempo deben ser unos 5 segundos más que el anterior = ", time.time() - t1)
                resultados.write("Tiempo hasta que se arrancó = " + str(time.time() - t1) + "\n")
                t1 = time.time()
            archivo = open("prioridad_bt.txt","w")
            archivo.write("comunicacion")
            print ("Devolvemos la prioridad a la comunicacion")
            archivo.close()





def generate_svg(src_size, inference_size, inference_box, objs, labels, text_lines):
    global nCoches

    dwg = svgwrite.Drawing('', size=src_size)
    src_w, src_h = src_size
    inf_w, inf_h = inference_size
    box_x, box_y, box_w, box_h = inference_box
    scale_x, scale_y = src_w / box_w, src_h / box_h

#    pygame.init()
 #   pygame.font.init()
  #  font = pygame.font.SysFont('Arial', 20)
   # size = width, height = (480, 640)

    #try:
     # display = pygame.display.set_mode((height, width), 0)
    #except pygame.error as e:
     # sys.stderr.write("\nERROR: Unable to open a display window. Make sure a monitor is attached and that "
      #      "the DISPLAY environment variable is set. Example: \n"
       #     ">export DISPLAY=\":0\" \n")
      #raise e

    #size = h, w = (height, width)
    #blue = (0, 0, 255)
    #white = (255, 255, 255)
    #red = pygame.Color(255, 0, 0)
    #3green = (0, 255, 0)
    #car_position = [(height/2 - height/30, width/2 - width/30), (height/2 + height/30, width/2 - width/30), (height/2 + height/30, width/2 + width/30), (height/2 - height/30, width/2 + width/30)]

    #dist_max = 15 #distancia maxima a la que podemos representar un coche

    #carsim = pygame.Surface(size)
    #carsim.fill((130, 130, 130))
    #pygame.draw.polygon(carsim, blue,  car_position)
    #pygame.draw.line(carsim, white, (height/5, 0), (height/5, width), 2)
    #pygame.draw.line(carsim, white, (2*height/5, 0), (2*height/5, width), 2)
    #pygame.draw.line(carsim, white, (3*height/5, 0), (3*height/5, width), 2)
    #pygame.draw.line(carsim, white, (4*height/5, 0), (4*height/5, width), 2)

    for y, line in enumerate(text_lines, start=1):
        shadow_text(dwg, 10, y*20, line)
    for obj in objs:
        x0, y0, x1, y1 = list(obj.bbox)
        if labels.get(obj.id, obj.id) == 'car':
            nCoches = np.loadtxt('nCoches.txt')
            nCoches = int(nCoches)
            nCoches += 1
            archivo = open("nCoches.txt","w")
            archivo.write(str(nCoches))
            archivo.close()

            print(x0, x1, y0, y1)
            #print_simulation(x0, y0, x1, y1, carsim, display, dist_max)
            semaforo_mode(x0, y0, x1, y1, "10")
        # Relative coordinates.
        x, y, w, h = x0, y0, x1 - x0, y1 - y0
        # Absolute coordinates, input tensor space.
        x, y, w, h = int(x * inf_w), int(y * inf_h), int(w * inf_w), int(h * inf_h)
        # Subtract boxing offset.
        x, y = x - box_x, y - box_y
        # Scale to source coordinate space.
        x, y, w, h = x * scale_x, y * scale_y, w * scale_x, h * scale_y
        percent = int(100 * obj.score)
        label = '{}% {}'.format(percent, labels.get(obj.id, obj.id))
        shadow_text(dwg, x, y - 5, label)
        dwg.add(dwg.rect(insert=(x,y), size=(w, h),
                        fill='none', stroke='red', stroke_width='2'))

    #display.blit(carsim, (0, 0))
    #pygame.display.flip()

    return dwg.tostring()

class BBox(collections.namedtuple('BBox', ['xmin', 'ymin', 'xmax', 'ymax'])):
    """Bounding box.
    Represents a rectangle which sides are either vertical or horizontal, parallel
    to the x or y axis.
    """
    __slots__ = ()

def get_output(interpreter, score_threshold, top_k, image_scale=1.0):
    """Returns list of detected objects."""
    boxes = common.output_tensor(interpreter, 0)
    category_ids = common.output_tensor(interpreter, 1)
    scores = common.output_tensor(interpreter, 2)

    def make(i):
        ymin, xmin, ymax, xmax = boxes[i]
        return Object(
            id=int(category_ids[i]),
            score=scores[i],
            bbox=BBox(xmin=np.maximum(0.0, xmin),
                      ymin=np.maximum(0.0, ymin),
                      xmax=np.minimum(1.0, xmax),
                      ymax=np.minimum(1.0, ymax)))
    return [make(i) for i in range(top_k) if scores[i] >= score_threshold]

def main():
    width, height = 300, 200
    temperaturas = []
    archivo = open("prioridad_bt.txt","w")
    archivo.write("comunicacion")
    archivo.close()

    resultados = open("result_detect.txt", "w")

    #knownSemaforos = [["7C:D9:5C:B1:C2:BB", 0, 0.5, 0, 0, 0], ["7C:D9:5C:B1:C6::F3", 0, 0.5, 0, 0, 0]]

    default_model_dir = '../all_models'
    default_model = 'mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite'
    default_labels = 'coco_labels.txt'
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help='.tflite model path',
                        default=os.path.join(default_model_dir,default_model))
    parser.add_argument('--labels', help='label file path',
                        default=os.path.join(default_model_dir, default_labels))
    parser.add_argument('--top_k', type=int, default=3,
                        help='number of categories with highest score to display')
    parser.add_argument('--threshold', type=float, default=0.5,
                        help='classifier score threshold')
    parser.add_argument('--videosrc', help='Which video source to use. ',
                        default='/dev/video1')
    parser.add_argument('--videofmt', help='Input video format.',
                        default='raw',
                        choices=['raw', 'h264', 'jpeg'])
    args = parser.parse_args()

    print('Loading {} with {} labels.'.format(args.model, args.labels))
    interpreter = common.make_interpreter(args.model)
    interpreter.allocate_tensors()
    labels = load_labels(args.labels)

    w, h, _ = common.input_image_size(interpreter)
    inference_size = (w, h)
    # Average fps over last 30 frames.
    fps_counter  = common.avg_fps_counter(30)

    def user_callback(input_tensor, src_size, inference_box):
      nonlocal fps_counter
      global nCoches
      global tpo

      out = open("out.txt", "w")
      start_time = time.monotonic()
      common.set_input(interpreter, input_tensor)
      interpreter.invoke()
      # For larger input image sizes, use the edgetpu.classification.engine for better performance
      objs = get_output(interpreter, args.threshold, args.top_k)
      end_time = time.monotonic()
      text_lines = [
          'Inference: {:.2f} ms'.format((end_time - start_time) * 1000),
          'FPS: {} fps'.format(round(next(fps_counter))),
      ]
      print(' '.join(text_lines))
      #print ("Diferencia de tiempos = ", time.time() - tpo)
      tpo = time.time()
      print ("nCoches main = ", nCoches)
      temp = int(load_temp())/1000
      print (temp)
      temperaturas.append(temp)
      for t in temperaturas:
          out.write(str(t) + "\n")

      return generate_svg(src_size, inference_size, inference_box, objs, labels, text_lines)

    result = gstreamer.run_pipeline(user_callback,
                                    src_size=(640, 480),
                                    appsink_size=inference_size,
                                    videosrc=args.videosrc,
                                    videofmt=args.videofmt)

if __name__ == '__main__':
    main()
