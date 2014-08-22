from argparse import ArgumentParser

def parse_arguments():
    """ Process command line arguments -> arg dict() """
    parser = ArgumentParser(description='Argument Parser Template')
    parser.add_argument('-b', '--basic', help='basic arg consuming option')
    parser.add_argument('-v', '--verbose', help='increase output verbosity, flag',
                        action='store_true')
    parser.add_argument('-g', '--greedy', help='greedy narg=* arg',
                        nargs='*')
    parser.add_argument('-c', '--choices', help='choices demonstration',
                        choices=['list', 'of', 'choices'])
    parser.add_argument('-s', '--string', help='string coercion arg',
                        type=str)
    parser.add_argument('-i', '--integer', help='integer coercion arg',
                        type=int)
    parser.add_argument('-f', '--float', help='float coercion arg',
                        type=float)
    #parser.add_argument('-r', '--required', help='required example arg',
    #                    required=True)

    args = parser.parse_args()

    return args


def main():
    args = parse_arguments()

    # Do stuff with args
    if args.verbose:
        print 'verbosity flag enabled'
    if args.basic:
        print 'Basic arg is type: %s' % type(args.basic)
    if args.greedy:
        print args.greedy
    if args.choices:
        print 'Congratulations! You chose %s' % args.choices
    if args.string:
        print 'Your arg is a %s' % type(args.string)
    if args.integer:
        print 'Your arg is a %s' % type(args.integer)
    if args.float:
        print 'Your arg is a %s' % type(args.float)


if __name__ == '__main__':
    main()

