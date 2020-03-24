# March 30 Lecture

All together, there's about 74 minutes of videos here, rather than the
usual 50.  Rather that split it up, I'll make Wed/Fri lectures shorter
to compensate.

## 1. Animated Counter

### Watch: [12-minute video](https://youtu.be/3pbk0kLkHOs)

### Practice: Motion

Copy/paste the following example and run it:

```python
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.core.display import HTML
from time import time

fig, ax = plt.subplots(figsize=(6,6))

circ = plt.Circle((0, 0), 0.1, facecolor="red", zorder=1)
ax.add_artist(circ)
rect = plt.Rectangle((0, 0.3), 1, 0.1, facecolor="black", zorder=2)
ax.add_artist(rect)

def draw_frame(frame_num):
    circ.center = (frame_num*0.1, 0.5)

anim = FuncAnimation(fig, draw_frame, frames=10, interval=250)
t0 = time()
html = anim.to_html5_video()
t1 = time()
print("Seconds to generate:", t1-t0)
plt.close(fig)
HTML(html)
```

Now attempt to make the following changes:
1. make the ball fall from the top to the bottom of the screen (in the x,y tuple for `circ.center`, the y portion could get smaller as we advance through the frames)
2. make the red ball appear in front of the black bar instead of behind by modifying the `zorder` of one or both shapes
3. make the animation smoother, but not longer, by (a) increasing the frames, (b) decreasing the interval between frames, (c) changing the formula for `circ.center` so that the ball moves by less that 0.1 per frame

It ought to look something like [goal.mp4](goal.mp4).

After the last change, how long did it take to generate the animation?

## 2. Frames, Intervals, and Debugging

### Watch: [8-minute video](https://youtu.be/G1VWVlxWTWA)

### Practice: Percent of Time

Copy/paste the following example:

```python
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.core.display import HTML, display
from time import time

fig, ax = plt.subplots(figsize=(6,6))

circ = plt.Circle((0, 0), 0.1, facecolor="red", zorder=3)
ax.add_artist(circ)
rect = plt.Rectangle((0, 0.3), 1, 0.1, facecolor="black", zorder=2)
ax.add_artist(rect)

seconds = 2
fps = 100 # frames-per second
frame_count = fps*seconds

def draw_frame(frame_num):
    percent = frame_num / frame_count
    if percent < 0.5:
        y = ????
    else:
        y = ????
    circ.center = (0.5, y)

debug_frame = None    

if debug_frame != None:
    draw_frame(debug_frame)
else:
    anim = FuncAnimation(fig, draw_frame, frames=frame_count, interval=1000/fps)
    t0 = time()
    html = anim.to_html5_video()
    t1 = time()
    print("Seconds to generate:", t1-t0)
    plt.close(fig)
    display(HTML(html))
```

Complete it so that:
1. for the first half of the video, the ball is falling from the top to the bottom
2. for the second half of the video, the ball should be bouncing from the bottom back up

It ought to look something like [goal-part2.mp4](goal-part2.mp4).

**Suggestion:** it can be hard to figure out the right equations for y
on the first attempt.  Consider reducing the `fps` rate temporarily so
you can quickly debug rough version of the video.  When it looks good,
increase it back up to make a smoother animation.

## 3. Complete Example: Animated Crime Map of Madison

In this mini-project example, I'll create an animated map showing
where crimes in Madison occur during a certain day.  There are three
parts:

1. grab crime data from city, and extract date information
2. using Google's geocoding API to convert addresses in the data to coordinates
3. use FuncAnimation and geopandas to create an animated map with a fade-out effect

### Watch A: [10-minute video](https://youtu.be/OlffsR6fHYk)
### Watch B: [24-minute video](https://youtu.be/7t2f6dQXotI)
### Watch C: [20-minute video](https://youtu.be/Mi4NklEE-Vw)
