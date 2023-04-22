import cv2
import numpy as np

def main():
    # Read the video file
    cap = cv2.VideoCapture('test.mp4')

    # Check if the video file was opened successfully
    if not cap.isOpened():
        print("Error opening video file")
        exit()

    # Read the first frame of the video
    ret, frame = cap.read()

    # Check if the frame was read successfully
    if not ret:
        print("Error reading video frame")
        exit()

    # Get the dimensions of the frame
    height, width, _ = frame.shape

    # Create a blank image to hold the snow effect
    snow = np.zeros((height, width, 3), np.uint8)

    # Set the video writer object to write the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (width, height))

    # Define the parameters for the snow particle simulation
    num_particles = 1000  # number of snow particles
    particle_size = 2  # size of each snow particle in pixels
    gravity : np.float64 = 0.1  # gravity constant
    wind : np.float64 = 0.1  # wind constant

    # Initialize the positions and velocities of the snow particles
    positions = np.random.randint(0, width, (num_particles, 2)).astype(np.float64)
    velocities = np.random.rand(num_particles, 2).astype(np.float64)
    print(positions)
    print(velocities)
    # Iterate over the frames of the video
    while cap.isOpened():
        # Read the current frame
        ret, frame = cap.read()

        # If the frame was not read successfully, break the loop
        if not ret:
            break

        # Clear the snow image
        snow[:] = 0

        # Update the positions and velocities of the snow particles
        positions += velocities
        velocities[:, 1] += gravity
        velocities[:, 0] += wind

        # Check if any of the particles have reached the bottom of the frame
        # If so, reset their position to the top of the frame and give them a new random velocity
        positions[positions[:, 1] > height, 1] = 0
        velocities[positions[:, 1] > height] = np.random.randn(np.sum(positions[:, 1] > height), 2)

        # Cast the positions and velocities to integers
        positions = positions.astype(np.int32)
        velocities = velocities.astype(np.int32)

        # Draw the snow particles on the image
        for x, y in positions:
            cv2.circle(snow, (x, y), particle_size, (255, 255, 255), -1)

        # Overlay the snow image on top of the original frame using alpha blending
        alpha = 0.5
        output = cv2.addWeighted(frame, 1 - alpha, snow, alpha, 0)

        # Write the resulting frame to the output video
        out.write(output)

if __name__ == "__main__":
    main()