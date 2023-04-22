import cv2

# Open the video file
video = cv2.VideoCapture('test.mp4')

# Check if the video was opened successfully
if not video.isOpened():
    print("Error opening video file")

# Read the video file frame by frame
success, frame = video.read()
# Create a VideoWriter object to write the modified frames to a new video file
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
print()
output_video = cv2.VideoWriter('output.mp4', fourcc, 30.0, (frame.shape[1], frame.shape[0]),True)

# Loop until the end of the video
while success:
    # Create a copy of the current frame
    ghost_frame = frame.copy()

    # Apply a transparency effect to the copy of the frame
    alpha = 0.99  # Adjust this value to control the level of transparency
    cv2.addWeighted(ghost_frame, alpha, frame, 1 - alpha, 0, frame)

    # Write the modified frame to the output video
    output_video.write(frame)
    print("process frame")
    # Read the next frame
    success, frame = video.read()

# Release the VideoCapture and VideoWriter objects
video.release()
output_video.release()
