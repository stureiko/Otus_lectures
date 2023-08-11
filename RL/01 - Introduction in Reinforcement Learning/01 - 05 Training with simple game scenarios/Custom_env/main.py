from Cure import Cure
from ActionSpace import ActionSpace
import matplotlib.pyplot as plt
from celluloid import Camera


def show_agent(epochs: int = 10):
    '''
    Show agent and environment
    :param epochs: animation time
    :return: sum reward
    '''
    fig = plt.figure()
    camera = Camera(fig)

    the_cure = Cure()

    # text box
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    sum_reward = 0
    rewards = []

    for i in range(epochs):
        action = ActionSpace().sample()
        observation, reward, done, _ = the_cure.step(action)
        sum_reward += reward
        rewards.append(reward)
        # show points
        bacteria_x, bacteria_y = the_cure.get_bacteria()
        plt.scatter(bacteria_x, bacteria_y, c='red')

        # покажем агента
        x, y, r = the_cure.get_position()
        plt.scatter(x, y, c='blue')
        fig = plt.gcf()
        ax = fig.gca()
        circle = plt.Circle((x, y), r, color='b', fill=False)
        ax.add_patch(circle)

        text_str = '\n'.join((
            r'epoch=%d' % (i,),
            r'points=%d' % (reward,),
        ))

        ax.text(0.05, 0.95, text_str, transform=ax.transAxes, fontsize=14,
                verticalalignment='top', bbox=props)
        camera.snap()
    plt.show()

    the_cure.close()
    animation = camera.animate()
    animation.save('celluloid_minimal.gif', writer='imagemagick')
    return sum_reward


def main():
    print(f'Итоговая награда: {show_agent()}')


if __name__ == '__main__':
    main()
